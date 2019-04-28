from beefcafe_auth.models import Certificate
def get_user(dn):
    user = Certificate.objects.get(dn=dn).user
    user_dict = {'username': user.username, 'first_name': user.first, 'last_name': user.last}
    return user_dict

