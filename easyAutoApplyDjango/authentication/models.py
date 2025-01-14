from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    wix_id = models.CharField(max_length=255) #, blank=True, null=True

    def __str__(self):
        if self.email and self.wix_id:
            return f"{self.username} (Email: {self.email}, Wix ID: {self.wix_id})"
        elif self.email:
            return f"{self.username} (Email: {self.email})"
        elif self.wix_id:
            return f"{self.username} (Wix ID: {self.wix_id})"
        else:
            return self.username