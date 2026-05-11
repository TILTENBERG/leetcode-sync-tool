from github import Github
from github.GithubException import GithubException
import config
import time

class GitHubClient:
    def __init__(self):
        if not config.GITHUB_PAT:
            raise ValueError("GITHUB_PAT is not set.")
        self.g = Github(config.GITHUB_PAT)
        self.user = self.g.get_user()
        self.repo_name = config.GITHUB_REPO
        self.repo = self._get_or_create_repo()

    def _get_or_create_repo(self):
        try:
            repo = self.user.get_repo(self.repo_name)
            print(f"Found existing repository: {self.repo_name}")
            return repo
        except GithubException as e:
            if e.status == 404:
                print(f"Repository {self.repo_name} not found. Creating it...")
                repo = self.user.create_repo(
                    self.repo_name, 
                    description="Competitive Programming Solutions synced automatically.", 
                    private=False
                )
                print(f"Created repository: {self.repo_name}")
                return repo
            else:
                raise e

    def get_existing_files(self):
        """Returns a set of file paths already in the repo to avoid duplicate work."""
        existing_files = set()
        try:
            commits = self.repo.get_commits()
            if commits.totalCount > 0:
                tree = self.repo.get_git_tree(commits[0].sha, recursive=True)
                for element in tree.tree:
                    if element.type == 'blob':
                        existing_files.add(element.path)
        except GithubException as e:
            # 404 or 409 means the repo is empty (no commits yet)
            if e.status not in (404, 409):
                print(f"Error fetching existing files: {e}")
        return existing_files

    def commit_file(self, path, content, commit_message, overwrite=False):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                try:
                    # Check if file exists
                    file = self.repo.get_contents(path)
                    if overwrite:
                        self.repo.update_file(path, commit_message, content, file.sha)
                        print(f"Updated: {path}")
                        return True
                    return False # File exists, skip
                except GithubException as e:
                    if e.status == 404:
                        self.repo.create_file(path, commit_message, content)
                        print(f"Pushed: {path}")
                        return True
                    raise e
            except GithubException as e:
                if e.status == 409 and attempt < max_retries - 1:
                    print(f"GitHub 409 Conflict for {path}. Retrying in 3 seconds...")
                    time.sleep(3)
                    continue
                print(f"Error committing {path}: {e}")
                return False
            except Exception as e:
                print(f"Error committing {path}: {e}")
                return False
        return False
