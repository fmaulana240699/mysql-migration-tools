# Generated by Django 5.0.2 on 2024-05-01 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_repointegration_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repointegration',
            name='token',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
