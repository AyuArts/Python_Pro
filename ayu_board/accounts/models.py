from django.db import models
from django.contrib.auth.models import User

def user_avatar_path(instance, filename):
    # Файли завантажуються в MEDIA_ROOT/avatars/user_<id>/<filename>
    return 'avatars/user_{0}/{1}'.format(instance.user.id, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField("Біографія", max_length=500, blank=True)
    birth_date = models.DateField("Дата народження", null=True, blank=True)
    location = models.CharField("Місце проживання", max_length=30, blank=True)
    avatar = models.ImageField("Аватар", upload_to=user_avatar_path, null=True, blank=True)

    def __str__(self):
        return self.user.username
