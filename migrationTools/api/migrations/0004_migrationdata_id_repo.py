# Generated by Django 5.0.2 on 2024-02-18 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_migrationdata_batch_version_migrationdata_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='migrationdata',
            name='id_repo',
            field=models.IntegerField(null=True),
        ),
    ]
