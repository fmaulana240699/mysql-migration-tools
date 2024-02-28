from github import Github

class githubHelper():
    def __init__(self, repo_name, file_location):
        self.github_token = ''
        self.repo_name = repo_name
        self.file_location = file_location

    def get_migration(self, full):
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        contents = repo.get_contents(full)
        return contents.decoded_content.decode()

    def get_last_commit_author(self):
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        commits = repo.get_commits(path=self.file_location)
        last_commit = commits[0]
        return last_commit.commit.author.name
    
    def compare_migration(self):
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        contents = repo.get_contents(self.file_location)
        return contents.name

    def get_list_file(self):
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        contents = repo.get_contents(self.file_location)
        list_file = []
        for x in contents:
            list_file.append(x.path)
        return list_file
# instance = githubHelper("fmaulana240699/mysql-migration-tools", "test.sql", "migrations-data/")
# instance.compare_migration()

