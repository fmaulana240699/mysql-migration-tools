from django.db import models

class repoIntegration(models.Model):
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    token = models.CharField(max_length=100)
    repo_url = models.CharField(max_length=100)

class migrationConfig(models.Model):
    id_repo = models.ForeignKey(repoIntegration, on_delete=models.CASCADE)
    folder_location = models.CharField(max_length=20)
    db_host = models.CharField(max_length=20, null=True)
    db_user = models.CharField(max_length=20, null=True)
    db_name = models.CharField(max_length=20, null=True)
    db_password = models.CharField(max_length=100, null=True)

class migrationData(models.Model):
    sql_query = models.TextField()
    status_query = models.CharField(max_length=10)
    author = models.CharField(max_length=20)
    error_log = models.TextField(null=True)
    file_name = models.CharField(max_length=200, null=True)
    batch_version = models.IntegerField(null=True)
    id_repo = models.ForeignKey(repoIntegration, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)