from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from account.forms import FormRegistration, FormAuthentification, Account, UserUpdateForm
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.forms import UserUpdateForm

from account.forms import FormRegistration, FormAuthentification

# Create your views here.

def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"already authenticated as {user.email}")
    context = {}

    if request.POST:
        form = FormRegistration(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect("home")
        else:
            context['registration_form'] = form
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request, *args, **kwargs):
    context= {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form = FormAuthentification(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect(request)
                if destination:
                    return redirect(destination)
                return redirect('home')
        else:
            context['login_form'] = form

    return render(request, "account/login.html", context)

def get_redirect(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
        return redirect
    
def profil_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)

    except Account.DoesNotExist:
        return HttpResponse("this is not an account")
    if account :
        context['username'] = account.username
        context['email'] = account.email
        context['hide_email'] = account.hide_email
        context['profile_picture'] = account.profile_picture.url if account.profile_picture else None
        context['id'] = account.id

        is_friend = False
        is_self = True
        user = request.user
        if user.is_authenticated and account != user:
            is_self = False
        elif not user.is_authenticated:
            is_self = False
        context ['is_friend'] = is_friend
        context['is_self'] = is_self
        context['BASE_URL'] = settings.BASE_URL
        return render(request, "account/profil.html", context)

@login_required
def update_user_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:profile', user_id=user.id)
    else:
        form = UserUpdateForm(instance=user)
    
    context = {'form': form}
    return render(request, 'account/update_account.html', context)