# Generated by Django 5.0.2 on 2024-02-18 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_migrationdata_error_log_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='migrationdata',
            name='batch_version',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='migrationdata',
            name='file_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
