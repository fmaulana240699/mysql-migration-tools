from celery import shared_task
from .models import migrationData, repoIntegration, migrationConfig
from .mysql_helper import mysqlHelper

@shared_task
def execute_remote_query(sql_query):
    testing = mysqlHelper(sql_query)
    try:
        testing.execute_query()
    except Exception as e:
        return e