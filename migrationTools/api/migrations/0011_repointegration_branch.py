# Generated by Django 5.0.2 on 2024-05-08 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_repointegration_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='repointegration',
            name='branch',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
