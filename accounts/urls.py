from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # The Homepage (Feed)
    path('', views.feed_view, name='feed'), 
    
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
]

