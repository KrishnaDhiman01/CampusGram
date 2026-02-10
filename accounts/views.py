from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('feed')
    else:
        form = UserCreationForm()
    # Note: The template path is now 'accounts/signup.html'
    return render(request, 'accounts/signup.html', {'form': form})

def feed_view(request):
    return render(request, 'accounts/base.html', {'title': 'Feed'})

def profile_view(request, username):
    # Get the user by their username (e.g., 'krishna')
    user_obj = get_object_or_404(User, username=username)
    
    # Send their data to the template
    return render(request, 'accounts/profile.html', {'user_obj': user_obj})

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        # Get data from the form
        user = request.user
        user.profile.bio = request.POST.get('bio')
        
        # Check if an image was uploaded
        if 'profile_img' in request.FILES:
            user.profile.profile_img = request.FILES['profile_img']
        
        user.profile.save()
        return redirect('profile', username=user.username)

    return render(request, 'accounts/edit_profile.html')

def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')