from beefcafe_auth.models import Certificate
def get_user(dn):
    certs = Certificate.objects.filter(dn=dn) 
    if not certs:
        return None
    # todo: make sure all users are the same under the list of certs. Shouldn't ever be a problem.
    user = certs[0].user
    user_dict = {'username': user.username, 'first_name': user.first, 'last_name': user.last}
    return user_dict

