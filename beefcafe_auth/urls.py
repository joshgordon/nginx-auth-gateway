from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^authcheck$', views.auth_check, name='auth_check'),
]

