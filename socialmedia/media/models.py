from django.db import models

from django.db import models
from django.conf import settings
from rest_framework.serializers import ValidationError
from socialmedia.common.models import BaseModel
class Post(BaseModel):

    slug = models.SlugField(primary_key=True, max_length=100)

    title = models.CharField(max_length=255)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(to = settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, null=True)


    def __str__(self):
        return self.slug


class Connection(models.Model):
    subscriber = models.ForeignKey(to = settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name="subscribers")
    target = models.ForeignKey(to = settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name="targets")

    class Meta:
        unique_together = ('subscriber', 'target')

    def clean(self):
        if self.subscriber == self.target:
            raise ValidationError({"subscriber": ("subscriber cannot be equal to target")})

    def __str__(self):
        return f"{self.subscriber.username}- {self.target.username}"