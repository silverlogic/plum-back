from django.db import models


class Family(models.Model):
    pass


class Parent(models.Model):
    family = models.ForeignKey('Family', related_name='parents')
    user = models.OneToOneField('users.User', related_name='parent')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def avatar(self):
        return self.user


class Kid(models.Model):
    family = models.ForeignKey('Family', related_name='kids')
    user = models.OneToOneField('users.User', related_name='kid', blank=True, null=True)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(null=True, blank=True)

    savings_match = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    allowance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return self.name
