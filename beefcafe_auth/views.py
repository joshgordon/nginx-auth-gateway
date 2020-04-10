from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import base64


from .models import *
# Create your views here.

def auth_check(request):
    site = request.META['HTTP_REQUESTED_SITE']
    site = Site.objects.get_or_create(fqdn=site)[0]
    try:
        issuer = request.META['HTTP_SSL_CLIENT_I_DN']
        dn = request.META['HTTP_SSL_CLIENT_S_DN']
    except KeyError:
        if site.allow_unauthorized:
            response = HttpResponse()
            response['authenticated'] = "false"
            response['authorized'] = "false"
            return response
        else:
            raise PermissionDenied

    cert = Certificate.objects.get_or_create(issuer=issuer, dn=dn)

    if cert[1]: 
        raise PermissionDenied
        return

    cert = cert[0]
    if cert.user.is_authorized(site):
        response = HttpResponse()
        response['first'] = cert.user.first
        response['last'] = cert.user.last
        response['username'] = cert.user.username
        response['auth_b64'] = base64.b64encode((cert.user.username + ":").encode("UTF-8")).decode("UTF-8")
        response['authenticated'] = "false"
        response['authorized'] = "false"
        return response
    else:
        raise PermissionDenied
