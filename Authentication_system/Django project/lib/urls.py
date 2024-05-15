from django.urls import path
from . import views

urlpatterns = [
    path('Signup/',views.Signup, name='Signup'),
    path('Signin/',views.Signin, name='Signin'),
    path('Signin/forgot_password/',views.forgotten_password,name='fpassword'),
    path('new_password/<int:idlib>/',views.forgotten_password1,name='newPassword'),
    path('Signup/confirm',views.confirm_library,name='confirm'),
    path('Home/',views.home,name='Home'),
    path('Home/Logout/', views.logout_lib,name='Logout'),
]