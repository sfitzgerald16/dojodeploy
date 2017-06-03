from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^secrets/', views.secrets, name='secrets'),
    url(r'^create/', views.create, name='create'),
    url(r'^like/(?P<id>\d+)*$', views.like, name='like'),
    url(r'^delete/(?P<id>\d+)*$', views.delete, name='delete'),
    url(r'^popular/', views.popular, name='popular'),
]
