from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login

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