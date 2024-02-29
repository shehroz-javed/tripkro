from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    email = models.EmailField(max_length=150, unique=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=13)
    term_condition = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone"]

    # default_manager = models.Manager()
    # objects = UserModelManager()

    def __str__(self):
        return f"{self.id}-{self.email}"

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"
        return super().save(*args, **kwargs)
