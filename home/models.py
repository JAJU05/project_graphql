from django.db import models
from django.db.models import CharField, DateTimeField, Model, ImageField


class News(Model):
    title = CharField(max_length=255)
    description = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    image = ImageField(null=True, blank=True)


