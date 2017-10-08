# nginx-auth-gateway

This is a simple django-based app that accepts requests from nginx's
[auth\_request](https://www.nginx.com/resources/admin-guide/restricting-access-auth-request/)
directive with two-way ssl client cert information and the site that's attempting to be accessed 
in it and passes back an authorization decision. 

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
