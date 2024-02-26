from django.db import models

class migrationData(models.Model):
    sql_query = models.TextField()
    status_query = models.BooleanField(null=True)
    author = models.CharField(max_length=20)
    error_log = models.TextField(null=True)
    file_name = models.CharField(max_length=200, null=True)
    batch_version = models.IntegerField(null=True)
    # id_repo = models.ForeignKey(Barang, on_delete=models.CASCADE, null=True)
    id_repo = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class migrationConfig(models.Model):
    folder_name = models.CharField(max_length=20)
    repo_name = models.CharField(max_length=20)

class repoIntegration(models.Model):
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    token = models.CharField(max_length=100)
    repo_url = models.CharField(max_length=100)

'''
#table migration_data
sql_query
status_query
author
error_log
migration_id
'''