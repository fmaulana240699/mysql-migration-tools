from celery import shared_task
from .models import migrationData, repoIntegration, migrationConfig
from .mysql_helper import mysqlHelper
from .slack_helper import SendNotif

@shared_task
def execute_remote_query(sql_query, id_repo, history_id, batch_version):
    creds = migrationConfig.objects.get(id_repo=id_repo)
    creds.decrypt()
    testing = mysqlHelper(sql_query, creds.db_host, creds.db_user, creds.db_password, creds.db_name)
    repo_integration_instance = repoIntegration.objects.get(pk=id_repo)
    try:
        testing.execute_query(batch_version)
        migrationData.objects.filter(id=history_id).update(status_query="success", id_repo=repo_integration_instance, db_name=creds.db_name)
        notif = SendNotif(creds.pk, creds.db_name, creds.author, "-", "Success")
        notif.slack()
    except Exception as e:
        migrationData.objects.filter(id=history_id).update(status_query="Error", error_log=str(e), id_repo=repo_integration_instance, db_name=creds.db_name)
        print("Error Gan")
        notif = SendNotif(creds.pk, creds.db_name, creds.author, e, "Error")
        notif.slack()
        return e

#