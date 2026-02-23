import requests
import base64
from gh_repo_inspector.utils.logging_config import get_logger

logger = get_logger(__name__)

class GitHubClient:
    def __init__(self, token=None):
        self.token = token
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({"Authorization": f"token {self.token}"})
        else:
            logger.warning("No GITHUB_TOKEN provided. Running in anonymous mode. Rate limits will be low.")

    def _handle_response(self, response):
        if response.status_code == 403 and "rate limit exceeded" in response.text.lower():
            logger.error("GitHub API rate limit exceeded.")
            response.raise_for_status()
        elif response.status_code == 401:
            logger.error("GitHub API authentication error. Check your token.")
            response.raise_for_status()
        elif response.status_code == 404:
            logger.error(f"Resource not found: {response.url}")
            return None
        response.raise_for_status()
        return response.json()

    def get_repo_info(self, repo_url):
        # Extract owner and repo from URL
        parts = repo_url.rstrip("/").split("/")
        if len(parts) < 2:
            raise ValueError(f"Invalid repo URL: {repo_url}")
        owner, repo = parts[-2], parts[-1]
        if repo.endswith(".git"):
            repo = repo[:-4]
        return owner, repo

    def get_commits(self, owner, repo, since=None, until=None):
        commits = []
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {"per_page": 100}
        if since:
            params["since"] = since

        while url:
            response = self.session.get(url, params=params)
            data = self._handle_response(response)
            if data is None:
                break
                
            for commit in data:
                commit_date_str = commit['commit']['author']['date']
                # Pendulum is better here but for now just basic comparison or trust 'since'
                # Actually we should filter by 'until' in memory if provided
                if until and commit_date_str > until:
                    continue
                commits.append(commit)
            
            if "next" in response.links:
                url = response.links["next"]["url"]
                params = {} # Params are already in the next URL
            else:
                url = None
        
        logger.info(f"Retrieved {len(commits)} commits for {owner}/{repo}")
        return commits

    def get_commit_detail(self, owner, repo, sha):
        url = f"{self.base_url}/repos/{owner}/{repo}/commits/{sha}"
        response = self.session.get(url)
        return self._handle_response(response)

    def get_readme(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}/readme"
        response = self.session.get(url)
        data = self._handle_response(response)
        if data and "content" in data:
            return base64.b64decode(data["content"]).decode("utf-8")
        return None
