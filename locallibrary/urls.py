from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^login/', views.login, name='login'),
    url(r'^postsign/', views.postsign, name='postsign'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^postsignup/', views.postsignup, name='postsignup'),
    url(r'^create/', views.create, name='create'),
    url(r'^postcreate/', views.postcreate, name='postcreate'),
    url(r'^check/', views.check, name='check'),

]
