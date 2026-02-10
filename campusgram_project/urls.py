from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line connects the main project to your 'accounts' app
    path('', include('accounts.urls')), 
]