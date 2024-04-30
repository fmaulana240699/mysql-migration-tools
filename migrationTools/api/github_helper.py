from github import Github

class githubHelper():
    def __init__(self, repo_name, file_location, github_token=None):
        self.github_token = github_token
        self.repo_name = repo_name
        self.file_location = file_location

    def get_migration(self, full):
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        contents = repo.get_contents(full)
        return contents.decoded_content.decode()

    def get_last_commit_author(self):
        try:
            g = Github(self.github_token)
            repo = g.get_repo(self.repo_name)
            commits = repo.get_commits(path=self.file_location)
            last_commit = commits[0]
            return last_commit.commit.author.name
        except Exception as e:
            print("An error occurred:", e)
            return e      
    
    def compare_migration(self):
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        contents = repo.get_contents(self.file_location)
        return contents.name

    def get_list_file(self):
        try:
            g = Github(self.github_token)
            repo = g.get_repo(self.repo_name)
            contents = repo.get_contents(self.file_location)
            list_file = []
            for x in contents:
                list_file.append(x.path)
            return list_file
        except Exception as e:
            print("An error occurred:", e)
            return e

instance = githubHelper("fmaulana240699/mysql-migration-tools", "migrations-data")
print(instance.get_last_commit_author())

