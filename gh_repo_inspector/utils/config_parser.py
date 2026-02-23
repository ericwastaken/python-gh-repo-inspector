import yaml
import os
import re
from gh_repo_inspector.utils.logging_config import get_logger

logger = get_logger(__name__)

def load_config(config_path):
    """
    Loads and validates the YAML configuration file.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML: {e}")
            
    if not config or 'repos' not in config or not isinstance(config['repos'], list):
        raise ValueError("Config must contain a 'repos' list.")
        
    validated_repos = []
    for i, repo in enumerate(config['repos']):
        validated_repo = validate_repo_config(repo, i)
        validated_repos.append(validated_repo)
        
    config['repos'] = validated_repos
    return config

def validate_repo_config(repo, index):
    """
    Validates individual repository configuration.
    """
    required_fields = ['url', 'getMainReadme', 'getAllCommitMessages', 'getAllCommitFilenames']
    for field in required_fields:
        if field not in repo:
            raise ValueError(f"Repository at index {index} is missing required field: {field}")
            
    # Validate URL
    url = repo['url']
    if not re.match(r'https?://github\.com/[\w\-\.]+ /[\w\-\.]+', url):
        # Slightly more relaxed regex but checks for basic github structure
        if not url.startswith("https://github.com/"):
            raise ValueError(f"Invalid GitHub URL at index {index}: {url}")

    # Set defaults for optional fields
    if 'dateRange' not in repo:
        repo['dateRange'] = "last 30 days"
        
    if 'authorFilter' in repo:
        try:
            re.compile(repo['authorFilter'])
        except re.error:
            raise ValueError(f"Invalid regex in authorFilter at index {index}: {repo['authorFilter']}")
            
    return repo
