from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse


from .models import *
# Create your views here.

def auth_check(request):
    try:
        issuer = request.META['HTTP_SSL_CLIENT_I_DN']
        dn = request.META['HTTP_SSL_CLIENT_S_DN']
        site = request.META['HTTP_REQUESTED_SITE']
    except KeyError:
        raise PermissionDenied

    cert = Certificate.objects.get_or_create(issuer=issuer, dn=dn)

    if cert[1]: 
        raise PermissionDenied
        return

    cert = cert[0]
    if cert.user.is_authorized(Site.objects.get_or_create(fqdn=site)[0]):
        response = HttpResponse()
        response['first'] = cert.user.first
        response['last'] = cert.user.last
        response['username'] = cert.user.username
        return response
    else:
        raise PermissionDenied
