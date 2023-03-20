#!/usr/local/autopkg/python
import subprocess
import plistlib
from autopkglib import Processor, ProcessorError

__all__ = ["GitRepoInfoProcessor"]

class GitRepoInfoProcessor(Processor):
    description = ("Outputs the current Git repo SHA and URL.")
    input_variables = {
        "GIT_REPO_PATH": {
            "required": True,
            "description": ("Path to the Git repository.")
        }
    }
    output_variables = {
        "GIT_REPO_SHA": {
            "description": ("The current Git repository SHA.")
        },
        "GIT_REPO_URL": {
            "description": ("The URL of the Git repository.")
        }
    }

    def get_git_repo_info(self, repo_path):
        try:
            git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_path).decode().strip()
            git_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], cwd=repo_path).decode().strip().replace('.git', '')
        except subprocess.CalledProcessError as e:
            raise ProcessorError("Could not get Git repository info: %s" % e)
        
        return git_sha, git_url

    def main(self):
        git_repo_path = self.env["GIT_REPO_PATH"]

        git_sha, git_url = self.get_git_repo_info(git_repo_path)

        self.output_variables["GIT_REPO_SHA"] = git_sha
        self.output_variables["GIT_REPO_URL"] = git_url

if __name__ == '__main__':
    processor = GitRepoInfoProcessor()
    processor.execute_shell()
