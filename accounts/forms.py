from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from thefacebook.settings import ALLOWED_SIGNUP_DOMAINS

from .models import Profile

User = get_user_model()


def SignupDomainValidator(value):
    if '*' not in ALLOWED_SIGNUP_DOMAINS:
        try:
            domain = value[value.index("@"):]
            if domain not in ALLOWED_SIGNUP_DOMAINS:
                raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(','.join(ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501

        except Exception:
            raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(','.join(ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501


def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name', 'status', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].validators.append(UniqueEmailValidator)
        self.fields['email'].validators.append(SignupDomainValidator)


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'name', 'email', 'status',
        )


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'concentration', 'relationship_status', 'sex', 'dob', 'phone_number',
            'high_school', 'screen_name','political_views', 'interests',
        )


class ProfilePictureEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('picture',)
