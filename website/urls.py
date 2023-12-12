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
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment_view, name='delete_appointment'),
    path('book-hospital-room/', views.book_hospital_room_view, name='book_hospital_room'),
    path('select-room/<str:branch_id>/', views.select_room_view, name='select_room'),
    path('booking-successful/<str:branch_id>/<str:room_id>/', views.booking_successful_view, name='booking_successful'),
    #Tanzuma
    path('my_appointments/', views.my_appointments_view, name='my_appointments'),
    path('my_room_bookings/', views.my_room_bookings_view, name='my_room_bookings'),
    path('delete_room_booking/<int:room_id>/', views.delete_room_booking_view, name='delete_room_booking'),
    #Ridhwan's path
    path('med_his_update/', views.update_medical_history, name='update_medical_history'),
    path('edit/', views.edit, name='edit'),
    path('delete/', views.delete_account, name='delete_account'),
    #walid's path
    path('review/', views.review_form, name='review_form'),
    path('review_success/',views.review_success,name= 'review_success'),
    path('all_hospitals/', views.all_hospitals, name='all_hospitals'),
    path('doctor_review/', views.doctor_review_form, name='doctor_review_form'),
    path('doctor_review_success/', views.doctor_review_success, name='doctor_review_success'),
    path('all_doctors/', views.all_doctors, name='all_doctors'),
]

