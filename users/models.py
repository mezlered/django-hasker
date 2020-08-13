from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.templatetags.staticfiles import static


def user_photo_path(instance, filename):
    return f'user_image/{filename}'


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    photo = models.ImageField(
        blank=True,
        upload_to=user_photo_path,
    )

    def save(self, *args, **kwargs):
        if not self.photo:
            self.photo = static("user/avatar.png")
            self.save()
        super().save(*args, **kwargs)
