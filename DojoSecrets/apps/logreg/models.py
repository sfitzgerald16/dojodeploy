# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z-\s]{2,}$')

class UserManager(models.Manager):
    def check_create(self, data):
        errors = []
        if not NAME_REGEX.match(data['first_name']):
            errors.append(['first_name', 'First name is invalid. Must contain at least two letters and no numbers.'])
        if not NAME_REGEX.match(data['last_name']):
            errors.append(['last_name', 'Last name is invalid. Must contain at least two letters and no numbers.'])
        if not EMAIL_REGEX.match(data['email']):
            errors.append(['email', 'Email is not a valid email.'])
        if len(data['password']) < 8:
            errors.append(['password', 'Password must be at least 8 characters.'])
        if data['confirm_pw'] != data['password']:
            errors.append(['password', 'Passwords do not match.'])
        if errors:
            return [False, errors]
        else:
            current_user = User.objects.filter(email=data['email'])
            if current_user:
                errors.append(['current_user', 'Unable to register, please use alternate information.'])
                return [False, errors]
            newUser = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], hashed_pass = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()))
            newUser.save()
            return [True, newUser]
    def check_log(self, data):
        errors = []
        current_user = User.objects.filter(email=data['email'])
        if not current_user:
            errors.append(['account', 'Email or password incorrect.'])
        elif not bcrypt.checkpw(data['password'].encode(), current_user[0].hashed_pass.encode()):
            errors.append(['account', 'Email or pasword incorrect.'])
        if errors:
            return [False, errors]
        else:
            return [True, current_user[0]]

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    hashed_pass = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
