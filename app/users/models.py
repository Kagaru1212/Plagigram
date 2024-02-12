from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


from .managers import CustomUserManager


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)
    biography = models.TextField(blank=True, verbose_name="Biography")
    followers = models.ManyToManyField('self', symmetrical=True)
    email = models.EmailField(_('email'), unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class Subscription(models.Model):
    follower = models.ForeignKey(User, related_name='subscribers', on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)

    objects = models.Manager()
