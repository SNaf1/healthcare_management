from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('loggedin/', views.loggedin_view, name='loggedin'),
    path('profile/', views.profile_view, name='profile'),
    # path('review/<str:hospital_id>/', views.review_form, name='review_form'),
    path('review/', views.review_form, name='review_form'),
    path('review_success/',views.review_success,name= 'review_success'),
    path('all_hospitals/', views.all_hospitals, name='all_hospitals'),
]
