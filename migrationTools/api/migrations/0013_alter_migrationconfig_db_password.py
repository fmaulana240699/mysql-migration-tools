# Generated by Django 5.0.2 on 2024-11-26 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_migrationconfig_folder_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='migrationconfig',
            name='db_password',
            field=models.CharField(max_length=200, null=True),
        ),
    ]