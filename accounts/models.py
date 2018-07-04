from __future__ import unicode_literals

import os

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    STATUS_CHOICES = (
        ('student', _('Student')),
        ('alumnus', _('Alumnus/Alumna')),
        ('faculty', _('Faculty')),
        ('staff', _('Staff')),
    )

    name = models.CharField(_('Name'), max_length=30)
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES, default='student')
    email = models.EmailField(_('Email'), unique=True)
    member_since = models.DateTimeField(_('Member Since'), auto_now_add=True)
    is_active = models.BooleanField(_('Active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_full_name(self):
        '''
        Returns the name, with a space in between.
        '''
        full_name = '%s' % (self.name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        short_name = self.name.split()
        return short_name[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


def get_filename_ext(filepath):
    """
    Return file name and extension.
    """
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def get_picture_filename(instance, filename):
    """
    Create path for the profile picture.
    """
    new_filename = instance.user.id
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile_pictures/{final_filename}".format(final_filename=final_filename)


class Profile(models.Model):

    RELATIONSHIP_STATUS_CHOICES = (
        ('empty', _('')),
        ('single', _('Single')),
        ('relationship', _('In a Relationship')),
        ('engaged', _('Engaged')),
        ('married', _('Married')),
        ('complicated', _('It\'s Complicated')),
    )

    SEX_CHOICES = (
        ('empty', _('')),
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    picture = models.ImageField(upload_to=get_picture_filename,
                                verbose_name=_('Upload a picture'),
                                blank=True,
                                null=True)

    # Info
    concentration = models.CharField(_('Concentration'), max_length=100, blank=True)
    relationship_status = models.CharField(_('Relationship Status'), max_length=20, choices=RELATIONSHIP_STATUS_CHOICES, default='empty', blank=True)
    sex = models.CharField(_('Sex'), max_length=20, choices=SEX_CHOICES, default='empty', blank=True)
    dob = models.DateField(blank=True, null=True)
    phone_number = models.CharField(_('Concentration'), max_length=100, blank=True)
    high_school = models.CharField(_('High School'), max_length=100, blank=True)
    screen_name = models.CharField(_('Screen Name'), max_length=100, blank=True)
    political_views = models.TextField(_('Political Views'), max_length=1000, blank=True)
    interests = models.CharField(_('Interests'), max_length=256, blank=True)

    # Activity
    pending_request = models.ManyToManyField(User, related_name='pending_requests', blank=True)
    sent_request = models.ManyToManyField(User, related_name='sent_requests', blank=True)
    friend = models.ManyToManyField(User, related_name='friends', blank=True)
    poke = models.ManyToManyField(User, related_name='pokes', blank=True)

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ('-created',)

    def __str__(self):
        return self.user.email

    def get_picture(self):
        default_picture = settings.STATIC_URL + 'img/profile_picture.jpg'
        if self.picture:
            return self.picture.url
        else:
            return default_picture



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
