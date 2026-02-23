import click
import os
import csv
import yaml
from dotenv import load_dotenv
from gh_repo_inspector.utils.logging_config import setup_logging, get_logger
from gh_repo_inspector.utils.config_parser import load_config
from gh_repo_inspector.utils.date_handler import parse_date_range, format_date_iso, format_date_for_display
from gh_repo_inspector.filters.author_filter import filter_by_author
from gh_repo_inspector.api.github_client import GitHubClient

logger = get_logger(__name__)

@click.command()
@click.option('--config', required=True, help='Path to YAML configuration file containing repo definitions')
@click.option('--outputDirectory', 'output_directory', required=True, help='Directory where structured output will be written')
@click.option('--logLevel', 'log_level', default='INFO', help='Logging level (DEBUG, INFO, WARNING, ERROR). Defaults to INFO')
@click.option('--env', help='Path to .env file')
def main(config, output_directory, log_level, env):
    """
    gh-repo-inspector: Retrieve commit metadata from a list of GitHub repositories.
    """
    setup_logging(log_level)
    if env:
        load_dotenv(dotenv_path=env)
    else:
        load_dotenv()
    
    token = os.getenv("GITHUB_TOKEN")
    client = GitHubClient(token)
    
    try:
        config_data = load_config(config)
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    elif not os.access(output_directory, os.W_OK):
        logger.error(f"Output directory is not writable: {output_directory}")
        return

    for repo_cfg in config_data['repos']:
        process_repository(client, repo_cfg, output_directory)

def process_repository(client, repo_cfg, output_root):
    repo_url = repo_cfg['url']
    try:
        owner, repo_name = client.get_repo_info(repo_url)
    except ValueError as e:
        logger.error(e)
        return

    logger.info(f"Processing repository: {owner}/{repo_name}")
    
    repo_output_dir = os.path.join(output_root, repo_name.lower())
    if not os.path.exists(repo_output_dir):
        os.makedirs(repo_output_dir)

    # 0. Save current repo config
    save_repo_config(repo_cfg, repo_output_dir)

    # 1. README
    if repo_cfg.get('getMainReadme'):
        try:
            readme_content = client.get_readme(owner, repo_name)
            if readme_content:
                with open(os.path.join(repo_output_dir, "README.md"), "w", encoding="utf-8") as f:
                    f.write(readme_content)
                logger.info(f"Saved README.md for {repo_name}")
        except Exception as e:
            logger.error(f"Failed to retrieve README for {repo_name}: {e}")

    # 2. Dates
    try:
        start_date, end_date = parse_date_range(repo_cfg.get('dateRange'))
        logger.info(f"Applied date range: {format_date_for_display(start_date)} to {format_date_for_display(end_date)}")
    except ValueError as e:
        logger.error(f"Invalid date range for {repo_name}: {e}")
        return

    # 3. Commits
    try:
        commits = client.get_commits(owner, repo_name, since=format_date_iso(start_date), until=format_date_iso(end_date))
    except Exception as e:
        logger.error(f"Failed to retrieve commits for {repo_name}: {e}")
        return

    # 4. Author Filter
    author_filter = repo_cfg.get('authorFilter')
    if author_filter:
        try:
            commits = filter_by_author(commits, author_filter)
        except ValueError as e:
            logger.error(e)
            return

    # 5. Output Commit Messages
    if repo_cfg.get('getAllCommitMessages'):
        write_commit_messages(commits, repo_output_dir)

    # 6. Output Commit Filenames
    if repo_cfg.get('getAllCommitFilenames'):
        write_commit_filenames(client, owner, repo_name, commits, repo_output_dir)

def save_repo_config(repo_cfg, output_dir):
    config_path = os.path.join(output_dir, "config.yml")
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(repo_cfg, f, default_flow_style=False)
        logger.info(f"Saved actual configuration to {config_path}")
    except Exception as e:
        logger.error(f"Failed to save config.yml: {e}")

def write_commit_messages(commits, output_dir):
    csv_path = os.path.join(output_dir, "commit_messages.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['commit_hash', 'author_date', 'author_name', 'subject_line', 'full_message'])
        for commit in commits:
            sha = commit['sha']
            commit_info = commit['commit']
            author_date = commit_info['author']['date']
            author_name = commit_info['author']['name']
            message = commit_info['message']
            subject_line = message.split('\n')[0]
            writer.writerow([sha, author_date, author_name, subject_line, message])
    logger.info(f"Wrote {len(commits)} rows to commit_messages.csv")

def write_commit_filenames(client, owner, repo_name, commits, output_dir):
    csv_path = os.path.join(output_dir, "commit_files.csv")
    file_count = 0
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['commit_hash', 'filename'])
        for commit in commits:
            sha = commit['sha']
            try:
                detail = client.get_commit_detail(owner, repo_name, sha)
                if detail and 'files' in detail:
                    for file in detail['files']:
                        writer.writerow([sha, file['filename']])
                        file_count += 1
            except Exception as e:
                logger.error(f"Failed to get details for commit {sha}: {e}")
    logger.info(f"Wrote {file_count} rows to commit_files.csv")

if __name__ == '__main__':
    main()
