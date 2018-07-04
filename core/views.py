from django.shortcuts import render


def home(request):
    if request.user.is_authenticated():
        friend_requests = request.user.pending_requests.all().count()
        pokes = request.user.pokes.all().count()
        friends = request.user.friends.all().count()
        return render(request, 'core/home.html', {
            'friend_requests': friend_requests,
            'pokes': pokes,
            'friends': friends,
        })
    else:
        return render(request, 'core/welcome.html', {})


def about(request):
    return render(request, 'core/about.html', {})


def contact(request):
    return render(request, 'core/contact.html', {})


def terms(request):
    return render(request, 'core/terms.html', {})


def privacy(request):
    return render(request, 'core/privacy.html', {})


def about(request):
    return render(request, 'core/about.html', {})


def faq(request):
    return render(request, 'core/faq.html', {})
