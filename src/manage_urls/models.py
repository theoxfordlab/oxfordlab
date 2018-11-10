from django.db import models
from users.models import User

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, related_name='groups', on_delete=models.CASCADE,
    )
    description = models.TextField(max_length=1023, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Url(models.Model):
    url = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, related_name='urls', on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group, related_name='urls', blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    description = models.TextField(max_length=1023, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

#
# class UrlGroup(models.Model):
#
#     description = models.TextField(max_length=1023, null=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)


# group = models.ForeignKey(
#     UrlGroup, related_name='urls', blank=True, null=True,
#     on_delete=models.SET_NULL,
# )
