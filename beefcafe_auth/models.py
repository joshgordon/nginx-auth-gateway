from django.db import models

# A single site (i.e. gogs.joshgordon.us) mostly just so I can limit stuff based on site.
class Site(models.Model):
    fqdn = models.CharField(max_length=100)

    def __str__(self):
        return self.fqdn


# a single certificate, tied to a single user.
class Certificate(models.Model):
    dn = models.CharField(max_length=300)
    issuer = models.CharField(max_length=300)
    user = models.ForeignKey('User', blank=True, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.dn + " I: " + self.issuer
    

# a group is a collection of sites so I can logically categorize them.
class Group(models.Model):
    name = models.CharField(max_length=30)
    sites = models.ManyToManyField(Site)

    def __str__(self):
        return self.name

# a single user, can have many certificates.
class User(models.Model):
    first = models.CharField(max_length=30)
    last = models.CharField(max_length=30)
    username = models.CharField(max_length=30)

    # superuser = let them access everything independent of group membership
    is_superuser = models.BooleanField()

    groups = models.ManyToManyField(Group, blank=True)
    def __str__(self):
        return self.first + " " + self.last + " : " + self.username

    def is_authorized(self, site):
        if self.is_superuser:
            return True
        if len(site.group_set.intersection(self.groups.all())) > 0:
            return True
            
