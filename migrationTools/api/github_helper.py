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
        print(contents.decoded_content.decode())

instance = githubHelper("fmaulana240699/mysql-migration-tools", "test.sql", "migrations-data/")
instance.get_migration()

