# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Secret, Like
from ..logreg.models import User

def index(request):
    return render(request, 'secrets/index.html')

def secrets(request):
    context = {
    'secrets': Secret.objects.all(),
    'userObj': User.objects.get(id=request.session['user']['id'])
    }
    return render(request, 'secrets/secrets.html', context)

def create(request):
    if request.POST:
        response = Secret.objects.check_create(request.POST, author=User.objects.get(id=request.session['user']['id']))
    if not response[0]:
        for message in response[1]:
            messages.error(request, message[1])
    return redirect('secrets:secrets')

def like(request, id):
    Like.objects.createlike(secret=Secret.objects.get(id=id), author=User.objects.get(id=request.session['user']['id']))
    page = request.META['HTTP_REFERER']
    print page
    return redirect(page)

def delete(request, id):
    Secret.objects.filter(id=id).delete()
    return redirect('secrets:secrets')

def popular(request):
    context = {
    'secrets': Secret.objects.all().annotate(Count('secret_like')),
    'userObj': User.objects.get(id=request.session['user']['id'])
    }
    return render(request, 'secrets/popular.html', context)
