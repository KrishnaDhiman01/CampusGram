from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import SignUpForm
from django.http import Http404
from django.contrib.auth.views import LoginView, LogoutView
from .models import Post, Follow, Like, Comment, Profile
from django.db.models import Q

def signup_view(request):
    if request.user.is_authenticated:
        raise Http404("Page not found")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('feed')
    else:
        form = SignUpForm()
    # Note: The template path is now 'accounts/signup.html'
    return render(request, 'accounts/signup.html', {'form': form})

def feed_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post.objects.filter(Q(user__in=following_users) | Q(user=request.user)).order_by('-created_at')

    liked_post_ids = set(
        Like.objects.filter(user=request.user, post__in=posts).values_list('post_id', flat=True)
    )

    return render(request, 'accounts/feed.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
    })

def profile_view(request, username):
    # Get the user by their username (e.g., 'krishna')
    user_obj = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user_obj).order_by('-created_at')
    is_following = False
    if request.user.is_authenticated and request.user != user_obj:
        is_following = Follow.objects.filter(follower=request.user, following=user_obj).exists()
    followers_count = Follow.objects.filter(following=user_obj).count()
    following_count = Follow.objects.filter(follower=user_obj).count()
    
    # Send their data to the template
    return render(request, 'accounts/profile.html', {
        'user_obj': user_obj,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count
    })

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

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)

@login_required
def like_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('feed')

@login_required
def follow_user_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if not created:
            follow.delete()
    return redirect('profile', username=username)

@login_required
def create_post_view(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        if image or caption:
            Post.objects.create(user=request.user, image=image, caption=caption)
            return redirect('feed')
        # If user submitted without content, just fall through to re-render form
    return render(request, 'accounts/create_post.html')

@login_required
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=request.user, post=post, text=text)
    return redirect('feed')

def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')