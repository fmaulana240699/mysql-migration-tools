# Generated by Django 5.0.2 on 2024-02-19 14:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_migrationdata_id_repo'),
    ]

    operations = [
        migrations.AddField(
            model_name='migrationdata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='migrationdata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
