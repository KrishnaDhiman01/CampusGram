from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # The Homepage (Feed)
    path('', views.feed_view, name='feed'), 
    
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
   path('logout/', views.logout_view, name='logout'),
    
    # Social features
    path('create-post/', views.create_post_view, name='create_post'),
    path('like/<int:post_id>/', views.like_post_view, name='like_post'),
    path('follow/<str:username>/', views.follow_user_view, name='follow_user'),
    path('comment/<int:post_id>/', views.add_comment_view, name='add_comment'),
    path('search/', views.search_users_view, name='search_users'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
]

