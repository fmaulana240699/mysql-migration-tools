from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from .secure_helper import encrypt_data, decrypt_data
from datetime import datetime

class Users(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Viewer', 'Viewer')
    ]
    id = models.CharField(max_length=5, primary_key=True, editable=False)
    fullname = models.CharField(max_length=40)
    username = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    password = models.CharField(max_length=100)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def __unicode__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        if not self.pk:
            count = Users.objects.count() + 1
            self.id = 'RK{:03d}'.format(count)
        super().save(*args, **kwargs)

class repoIntegration(models.Model):
    id = models.CharField(max_length=5, primary_key=True, editable=False)
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    token = models.CharField(max_length=400, null=True)
    branch = models.CharField(max_length=20, null=True)
    repo_url = models.CharField(max_length=100)
    author = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, to_field='username')

    def encrypt(self,raw_token):
        self.token=encrypt_data(raw_token)

    def decrypt(self):
        self.token=decrypt_data(self.token)

    def save(self, *args, **kwargs):
        if not self.pk:
            count = repoIntegration.objects.count() + 1
            self.id = 'RP{:03d}'.format(count)
        super().save(*args, **kwargs)

class migrationConfig(models.Model):
    id = models.CharField(max_length=6, primary_key=True, editable=False)
    id_repo = models.ForeignKey(repoIntegration, on_delete=models.CASCADE)
    folder_location = models.CharField(max_length=50)
    db_host = models.CharField(max_length=20, null=True)
    db_user = models.CharField(max_length=20, null=True)
    db_name = models.CharField(max_length=20, null=True)
    db_password = models.CharField(max_length=400, null=True)
    author = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, to_field='username')

    def encrypt(self,raw_password):
        self.db_password=encrypt_data(raw_password)

    def decrypt(self):
        self.db_password=decrypt_data(self.db_password)

    def save(self, *args, **kwargs):
        if not self.pk:
            count = migrationConfig.objects.count() + 1
            self.id = 'CFG{:03d}'.format(count)
        super().save(*args, **kwargs)

class migrationData(models.Model):
    id = models.CharField(max_length=12, primary_key=True, editable=False)
    sql_query = models.TextField(max_length=250)
    status_query = models.CharField(max_length=10, null=True)
    engineer_name = models.CharField(max_length=20)
    error_log = models.TextField(max_length=250, null=True)
    file_name = models.CharField(max_length=50, null=True)
    id_repo = models.ForeignKey(repoIntegration, on_delete=models.CASCADE)
    db_name = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            count = migrationData.objects.count() + 1
            today = datetime.now()
            formatted_date = today.strftime("%Y%m%d")
            self.id = formatted_date + '-{:03d}'.format(count)
        super().save(*args, **kwargs)
