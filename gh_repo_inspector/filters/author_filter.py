import re
from gh_repo_inspector.utils.logging_config import get_logger

logger = get_logger(__name__)

def filter_by_author(commits, author_regex):
    """
    Filters a list of commits by author name using a regex.
    """
    if not author_regex:
        return commits
        
    try:
        pattern = re.compile(author_regex)
    except re.error as e:
        logger.error(f"Invalid regex '{author_regex}': {e}")
        raise ValueError(f"Invalid author filter regex: {author_regex}")
        
    filtered_commits = []
    for commit in commits:
        # GitHub API commit structure: commit['commit']['author']['name']
        author_name = commit.get('commit', {}).get('author', {}).get('name', '')
        if pattern.search(author_name):
            filtered_commits.append(commit)
            
    logger.info(f"Filtered {len(commits)} commits to {len(filtered_commits)} using author filter '{author_regex}'")
    return filtered_commits
