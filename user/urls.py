from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.register_user, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('get-all-users', views.get_users, name='get-all-users')
]