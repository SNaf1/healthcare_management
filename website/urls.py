from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('loggedin/', views.loggedin_view, name='loggedin'),
    path('profile/', views.profile_view, name='profile'),
    # path('edit/', views.edit, name='edit'),
    path('edit/', views.edit, name='edit'),
    path('delete/', views.delete_account, name='delete_account'),

]
