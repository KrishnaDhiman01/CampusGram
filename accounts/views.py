from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from .forms import SignUpForm
from .models import Post, Follow, Like, Comment, Profile, Notification

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

    category_filter = request.GET.get('category')
    tag_filter = request.GET.get('tag')
    active_filter = None

    if category_filter:
        posts = Post.objects.filter(category=category_filter).order_by('-created_at')
        active_filter = f"Category: {category_filter}"
    elif tag_filter:
        clean_tag = tag_filter.replace('#', '')
        # Filter posts whose caption or category matches the tag
        posts = Post.objects.filter(
            Q(caption__icontains=clean_tag) | Q(category__icontains=clean_tag)
        ).order_by('-created_at')
        active_filter = f"Tag: #{clean_tag}"
    else:
        following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        posts = Post.objects.filter(Q(user__in=following_users) | Q(user=request.user)).order_by('-created_at')

    posts = posts.prefetch_related('comment_set', 'user__profile', 'like_set')

    liked_post_ids = set(
        Like.objects.filter(user=request.user, post__in=posts).values_list('post_id', flat=True)
    )

    # Static but highly clean & professional data for Campus Notice Board
    campus_notices = [
        {
            'icon': 'award',
            'title': 'Coding Competition Tomorrow',
            'detail': 'Organized by Coding Club. Starts at 10:00 AM in Lab 3. Exciting prizes!',
            'tag': 'Competition',
            'bg': 'hsl(215, 60%, 25%)',
            'text': '#fff'
        },
        {
            'icon': 'briefcase',
            'title': 'Placement Drive Next Week',
            'detail': 'Pre-placement talk by tech leaders on Monday. Mandatory for final years.',
            'tag': 'Placements',
            'bg': '#e3f2fd',
            'text': '#0d47a1'
        },
        {
            'icon': 'alert-circle',
            'title': 'Library Closed on Sunday',
            'detail': 'Annual system maintenance. Digital catalog offline from 8 AM to 6 PM.',
            'tag': 'Notice',
            'bg': '#fff3e0',
            'text': '#e65100'
        },
        {
            'icon': 'zap',
            'title': 'Tech Fest Registration Open',
            'detail': 'Register early for the early bird discount! Hackathons, web dev, and gaming.',
            'tag': 'Events',
            'bg': '#e8f5e9',
            'text': '#1b5e20'
        }
    ]

    # Trending Campus Tags
    trending_tags = [
        {'name': '#TechFest', 'category_name': 'Event', 'count': '18 posts'},
        {'name': '#Placements', 'category_name': 'Announcement', 'count': '12 posts'},
        {'name': '#StudyMaterial', 'category_name': 'Study Material', 'count': '25 posts'},
        {'name': '#LostAndFound', 'category_name': 'Lost & Found', 'count': '7 posts'},
        {'name': '#CampusLife', 'category_name': 'Fun Moment', 'count': '42 posts'},
    ]

    return render(request, 'accounts/feed.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
        'campus_notices': campus_notices,
        'trending_tags': trending_tags,
        'active_filter': active_filter,
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
        user.profile.department = request.POST.get('department', '')
        user.profile.year = request.POST.get('year', '')
        
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
        # Delete corresponding notification
        Notification.objects.filter(sender=request.user, post=post, notification_type='like').delete()
    else:
        # Create notification if liking other user's post
        if post.user != request.user:
            Notification.objects.create(
                recipient=post.user,
                sender=request.user,
                post=post,
                notification_type='like'
            )
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

@login_required
def follow_user_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if not created:
            follow.delete()
            # Delete corresponding notification
            Notification.objects.filter(sender=request.user, recipient=user_to_follow, notification_type='follow').delete()
        else:
            # Create notification
            Notification.objects.create(
                recipient=user_to_follow,
                sender=request.user,
                notification_type='follow'
            )
    return redirect('profile', username=username)

@login_required
def create_post_view(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        category = request.POST.get('category', 'Fun Moment')
        if image or caption:
            Post.objects.create(user=request.user, image=image, caption=caption, category=category)
            return redirect('feed')
        # If user submitted without content, just fall through to re-render form
    return render(request, 'accounts/create_post.html')

@login_required
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            comment = Comment.objects.create(user=request.user, post=post, text=text)
            # Create notification if comment is not by post owner
            if post.user != request.user:
                Notification.objects.create(
                    recipient=post.user,
                    sender=request.user,
                    post=post,
                    notification_type='comment'
                )
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')

@login_required
def search_users_view(request):
    query = request.GET.get('q', '')
    users = []
    if query:
        users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    return render(request, 'accounts/search.html', {'users': users, 'query': query})

@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('profile', username=request.user.username)

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    liked_post_ids = set()
    if request.user.is_authenticated and Like.objects.filter(user=request.user, post=post).exists():
        liked_post_ids.add(post.id)
    return render(request, 'accounts/post_detail.html', {'post': post, 'liked_post_ids': liked_post_ids})

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    # Mark all unread notifications as read when the page is visited
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return render(request, 'accounts/notifications.html', {'notifications': notifications})