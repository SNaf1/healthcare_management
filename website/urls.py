from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('loggedin/', views.loggedin_view, name='loggedin'),
    path('profile/', views.profile_view, name='profile'),
    path('book-appointment/', views.book_appointment_view, name='book_appointment'),
    path('select_date/<int:doctor_id>/', views.select_date_view, name='select_date'),
    path('select_time/<int:doctor_id>/<str:date>/', views.select_time_view, name='select_time'),
    path('confirm-payment/<int:doctor_id>/<str:date>/<str:time>/', views.confirm_payment_view, name='confirm_payment'),
    path('appointment-success/', views.appointment_success_view, name='appointment_success'),
    path('book-hospital-room/', views.book_hospital_room_view, name='book_hospital_room'),
    path('select-room/<str:branch_id>/', views.select_room_view, name='select_room'),
    path('booking-successful/<str:branch_id>/<str:room_id>/', views.booking_successful_view, name='booking_successful'),
]

