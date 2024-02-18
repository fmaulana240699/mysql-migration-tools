# Generated by Django 5.0.2 on 2024-02-18 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='migrationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sql_query', models.TextField()),
                ('status_query', models.BooleanField()),
                ('author', models.CharField(max_length=20)),
                ('error_log', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='repoIntegration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20)),
                ('token', models.CharField(max_length=100)),
                ('repo_url', models.CharField(max_length=100)),
            ],
        ),
    ]
