from github import Github

class githubHelper():
    def __init__(self, repo_name):
        self.github_token = ''
        self.repo_name = repo_name

    def get_migration(self):
        # auth = Auth.Token(self.github_token)
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        contents = repo.get_contents("README.md")
        print(contents)

instance = githubHelper()
instance.get_migration()

#'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'