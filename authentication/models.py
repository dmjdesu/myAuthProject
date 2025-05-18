from django.contrib.auth.models import AbstractUser
from oauth2_provider.models import Application
from django.db import models

class User(AbstractUser):
    allowed_applications = models.ManyToManyField(
        Application,
        related_name='allowed_users',        # Application.allowed_users で逆参照
        related_query_name='allowed_user',    # Application.objects.filter(allowed_user=...)
        blank=True,
        help_text="ユーザーがアクセスを許可されているクライアントアプリケーション"
    )
