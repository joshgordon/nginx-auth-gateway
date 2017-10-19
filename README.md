# nginx-auth-gateway

This is a simple django-based app that accepts requests from nginx's
[auth\_request](https://www.nginx.com/resources/admin-guide/restricting-access-auth-request/)
directive with two-way ssl client cert information and the site that's attempting to be accessed 
in it and passes back an authorization decision. 

Getting started
===============
You need to provide a few things for nginx and django. You'll need an ssl cert and a key, either from
let's encrypt, another CA (yours or another, doesn't matter) or self signed. Those should be called
`fullchain.pem` and `privkey.pem` (by default), but you can change it however you want by adjusting the volume
mount in `docker-compose.yml` and editing `default.conf` (to point at the new filenames.).

You'll also need your (or any, really) CA chain. I have my personal CAs in mine, in addition to some that I
don't control. The beautiful thing about this setup is that you don't have to trust every cert issued by the CA. 
I'm planning to add the LE CAs to my chain, so that I can use their certs to connect to my server. This should
be called `ca-chain.pem`.

After that, you can go about getting yourself bootstrapped with django. 

Getting yourself bootstrapped can be a bit tricky, since the admin panel for auth-gateway is behind nginx's
auth-gateway control, so you can't get in because auth-gateway doesn't know who you are, and you can't tell
auth-gateway who you are because you can't get in. Fortunately, this is an easy fix to bootstrap yourself
the first time. 

Port 80 is open and configured to forward to django by default (I don't advise running in prod this way, but
it's a fine way to bootstrap yourself.) 


Go ahead and do a docker-compose up -d, tweaking any config options that need tweaking. (I personally use
a single postgres container for all my services that need postgres, and a single nginx for everything.)

After that, run `./manage.py createsuperuser` to create the first user to sign into django. (Note the magic 
that's in manage.py to drop you in the container if you're not running in the container already!) 

After you've done this, go to http://localhost/admin (or whatever host/port you're running on) and sign in. 
Then go to https://localhost to get your certificate into auth-gateway. (it auto-adds certs that it sees) 
Then go to "Certificates" in the admin panel, click on your certificate, click the "+" next to "user", and
enter your user details. Save everything, and try going to https://localhost/admin. You'll need to sign in
again, but then everything should work. 

Go ahead and take the port 80 details out of default.conf and out of docker-compose.yml



Models
======

After you've done that, you can do ./manage.py createsuperuser
There's 4 models, as outlined below: 

Certificate
-----------

This is identified by a client cert's subject and issuer, and is also tied to a User...
These are auto-created when a new certificate is seen. 

Speaking of User...

User
----

This is one person, who can be identified by many certificates. Fields for First name, Last name,
and username are provided so they can be passed back to nginx to be passed back for use by a 
backend. 

Note there's a `is_superuser` field which, when set, will grant that user permissions to every site
automatically, much like django's `is_superuser` field on the user model.

A user also has a list of Groups.

Speaking of Groups....

Group
-----

A group is a name for the group and a list of sites that members of that group are allowed to access. 

Speaking of sites....

Site
----

A site is just an fqdn that defines a site that a user would try to access. It should just be the domain
name part of the request.

Configuring nginx
=================

nginx is really easy to get to work with this. In your server block, add this:

```
# you can also include auth_request inside a location block, with the auth_request_set in there as well.
auth_request /beefcafe_auth;
auth_request_set $auth_username $upstream_http_username;
auth_request_set $auth_last $upstream_http_last;
auth_request_set $auth_first $upstream_http_first;
location /beefcafe_auth {
    internal;
    proxy_pass http://{{ip of auth gateway}}/authcheck;
    proxy_pass_request_body off;
    proxy_set_header        Content-Length "";
    proxy_set_header ssl-client-i-dn $ssl_client_i_dn;
    proxy_set_header ssl-client-s-dn $ssl_client_s_dn;
    proxy_set_header requested-site $host;
}
```

Note that you'll need to include `ssl_client_certificate` and `ssl_verify_client on` in your ssl config. 

If you want to proxy the returned user's name and username, you'll have to set them in the location block:

```
location /headers {
    proxy_set_header auth-username $auth_username;
    proxy_set_header auth-first $auth_first;
    proxy_set_header auth-last $auth_last;
    proxy_pass https://postman-echo.com/get;
}
```

