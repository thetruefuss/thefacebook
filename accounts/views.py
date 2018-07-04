from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render

from thefacebook.decorators import ajax_required

from .forms import (ProfileEditForm, ProfilePictureEditForm, RegistrationForm,
                    UserEditForm)
from .models import Profile

User = get_user_model()


def register(request):
    """
    View the sign up page or create a new account.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            auth = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            auth_login(request, auth)
            return redirect('home')
        else:
            render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    """
    View the login page or perform login action.
    """
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                auth = authenticate(
                    email=email,
                    password=password,
                )
                if auth.is_active:
                    auth_login(request, auth)
                    return redirect('home')
                else:
                    return redirect('login')
            else:
                return redirect('login')
    else:
        return render(request, 'accounts/login.html', {})


@login_required
def profile(request):
    """
    View the user profile page.
    """
    if request.GET.get('id', None):
        user_id = int(request.GET.get('id', None))
        user = get_object_or_404(User, pk=user_id)
        profile = user.profile
    else:
        user = get_object_or_404(User, email=request.user.email)
        profile = user.profile

    friends_count = user.friends.all().count()

    return render(request, 'accounts/profile.html', {
        'user': user,
        'profile': profile,
        'friends_count': friends_count
    })


@login_required
def edit_info(request):
    """
    View the info edit page or post the form to change user/profile related info.
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)

        if user_form.is_valid():
            user_form.save()
        else:
            user_form = UserEditForm(instance=request.user)

        if profile_form.is_valid():
            profile_form.save()
        else:
            profile_form = ProfileEditForm(instance=request.user.profile)

        return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        user = request.user
        profile = user.profile
        friends_count = user.friends.all().count()

        return render(request, 'accounts/info_edit.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'user': user,
            'profile': profile,
            'friends_count': friends_count,
        })


@login_required
def edit_picture(request):
    """
    View the picture edit page or post the form to change profile picture.
    """
    if request.method == 'POST':
        profile_picture_form = ProfilePictureEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if profile_picture_form.is_valid():
            profile_picture_form.save()
        else:
            profile_picture_form = ProfilePictureEditForm(instance=request.user.profile)

        return redirect('profile')
    else:
        profile_picture_form = ProfilePictureEditForm(instance=request.user.profile)

        user = request.user
        profile = user.profile
        friends_count = user.friends.all().count()

        return render(request, 'accounts/picture_edit.html', {
            'user': user,
            'profile': profile,
            'friends_count': friends_count,
            'profile_picture_form': profile_picture_form,
        })


def search(request, board_slug=None):
    """
    Handles search functionality for all users.
    """
    if 'q' in request.GET:
        q = request.GET.get('q', None)
        search_resuls = User.objects.filter(name__icontains=q)

        paginator = Paginator(search_resuls, 15)
        page = request.GET.get('page')
        if paginator.num_pages > 1:
            p = True
        else:
            p = False
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        p_obj = users

        return render(request, 'accounts/search_resuls.html', {
            'page': page,
            'users': users,
            'p': p,
            'p_obj': p_obj,
        })
    else:
        return redirect('home')
