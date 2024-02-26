from github import Github

class githubHelper():
    def __init__(self, repo_name, file_name, file_location):
        self.github_token = ''
        self.repo_name = repo_name
        self.file_name = file_name
        self.file_location = file_location
        self.full_file_loc = file_location+file_name

    def get_migration(self):
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        contents = repo.get_contents(self.full_file_loc)
        return contents.decoded_content.decode()

    def get_last_commit_author(self):
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        commits = repo.get_commits(path=self.full_file_loc)
        last_commit = commits[0]
        return last_commit.commit.author.name
    
    def compare_migration(self):
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        contents = repo.get_contents(self.full_file_loc)
        return contents.name

# instance = githubHelper("fmaulana240699/mysql-migration-tools", "test.sql", "migrations-data/")
# instance.compare_migration()

