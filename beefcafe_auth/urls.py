from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^test$', views.auth_check, name='auth_check'),
]

