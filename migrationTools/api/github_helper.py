from github import Github

from github import Github

class githubHelper():
    def __init__(self, repo_name, file_location, branch, github_token=None):
        self.github_token =  github_token
        self.repo_name =  repo_name
        self.file_location = file_location
        self.branch = branch

    def get_migration(self, full):
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        contents = repo.get_contents(full, ref=self.branch)
        return contents.decoded_content.decode()

    def get_last_commit_author(self):
        try:
            g = Github(self.github_token)
            repo = g.get_repo(self.repo_name)
            commits = repo.get_commits(path=self.file_location, sha=self.branch)
            last_commit = commits[0]
            return last_commit.commit.author.name
        except Exception as e:
            print("An error occurred:", e)
            return e

    def compare_migration(self):
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_name)
        contents = repo.get_contents(self.file_location, ref=self.branch)
        return contents.name

    def get_list_file(self):
        try:
            g = Github(self.github_token)
            repo = g.get_repo(self.repo_name)
            contents = repo.get_contents(self.file_location, ref=self.branch)
            list_file = []
            for x in contents:
                list_file.append(x.path)
            return list_file
        except Exception as e:
            print("An error occurred:", e)
            return e

class ConnectionTesting():
    def __init__(self, repo_name, github_token, branch, file_location=None):
        self.github_token =  github_token
        self.repo_name =  repo_name
        self.branch = branch
        self.file_location = file_location

    def check(self):
        g = Github(self.github_token)
        try:
            test = g.get_user()
            test.login
            repo = g.get_repo(self.repo_name)
            branch = repo.get_branch(self.branch)
            return True
        except Exception as e:
            return False

    def check_folder(self):
        g = Github(self.github_token)
        try:
            test = g.get_repo(self.repo_name)
            print(test.get_contents(self.file_location, ref=self.branch))
            return True
        except Exception as e:
            print(e)
            return False