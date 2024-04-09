"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from RapidType.views import *

urlpatterns = [
    path('',test,name='test'),
    path('admin/', admin.site.urls),
    path('signup/',signup,name='signup'),
    path('profile/',profile,name='profile'),
    path('loginpage/',loginpage,name='loginpage'),
    path('logoutpage/',logoutpage,name='logoutpage'),
    path('save-test-result/', save_test_result, name='save_test_result'),
    path('get-random-text-prompt/', get_random_text_prompt, name='get_random_text_prompt'),
    path('leaderboard/',leaderboard,name='leaderboard'),
    path('generate-graph/', generate_graph, name='generate_graph')
]
