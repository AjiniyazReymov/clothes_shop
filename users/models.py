import uuid
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

from shared.models import BaseModel

ORDINARY_USER, MANAGER, ADMIN = ("ordinary_user", 'manager', 'admin')

class CustomUser(AbstractUser, BaseModel):
    USER_ROLES = (
        (ORDINARY_USER, ORDINARY_USER),
        (MANAGER, MANAGER),
        (ADMIN, ADMIN)
    )

    user_roles = models.CharField(max_length=31, choices=USER_ROLES, default=ORDINARY_USER)
    phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True)
    profile_picture = models.ImageField(default='default_picture.png', upload_to='user_photos/', null=True, blank=True,
                              validators=[
                                  FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heif'])])