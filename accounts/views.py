from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileUpdateForm



# Create your views here.
def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'accounts/register.html', {'form' : form})



@login_required
def author_profile(request, username):
    author = get_object_or_404(User, username=username)
    blogs = Post.objects.filter(author=author)
    
    try:
        profile = Profile.objects.get(user=author)
        #print(profile.bio)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=author)
    
    context = {'author': author, 'blogs': blogs, 'profile': profile}

    return render(request, 'accounts/profile.html', context)



@login_required
def profile_update(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile has been updated sucessfully")
            return redirect('profile', profile.user.username)
    else:
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/profile_update.html', {'profile_form': profile_form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile', user.username)
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/signin.html', {'form': form})

 


def user_logout(request):
    logout(request)
    return redirect('login')