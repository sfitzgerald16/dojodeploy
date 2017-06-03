# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..logreg.models import User

class SecretManager(models.Manager):
    def check_create(self, data, author):
        errors = []
        if len(data['secret']) < 2:
            errors.append(['secret', 'Message must be at least two characters.'])
        if errors:
            return [False, errors]
        else:
            newSecret = Secret(secret=data['secret'], author=author)
            newSecret.save()
            return [True]

class Secret(models.Model):
    secret = models.TextField(max_length=1000)
    author = models.ForeignKey('logreg.User', related_name='message', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def get_like_users(self):
        return User.objects.filter(author_like__secret=self)

    objects = SecretManager()

class LikesManager(models.Manager):
    def createlike(self, secret, author):
        newLike = Like(author=author, secret=secret)
        newLike.save()
        return [True]

class Like(models.Model):
    author = models.ForeignKey('logreg.User', related_name='author_like', on_delete=models.CASCADE)
    secret = models.ForeignKey('Secret', related_name='secret_like', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = LikesManager()
