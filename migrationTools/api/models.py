from django.db import models

class migrationData(models.Model):
    sql_query = models.TextField()
    status_query = models.BooleanField()
    author = models.CharField(max_length=20)
    error_log = models.TextField()
    # id_repo = models.ForeignKey(Barang, on_delete=models.CASCADE, null=True)


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