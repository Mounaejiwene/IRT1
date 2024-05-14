from django.urls import path
from . import views

urlpatterns = [
    path('Ajouter un livre/', views.ajouter_livre, name='add_book'),
    path('about/', views.about_page,name = 'about'),
    path('', views.liste_livres,name = 'Liste des livres'),
    path('book/<str:book_name>/',views.detail_livre, name='detail_livre'),
    path('recherche/', views.recherche, name='recherche'),
    path('Signup/',views.Signup, name='Signup'),
    path('Signin/',views.Signin, name='Signin'),
    path('Signin/forgot_password/',views.forgotten_password,name='fpassword'),
    path('new_password/<int:idlib>/',views.forgotten_password1,name='newPassword'),
    path('Signup/confirm',views.confirm_library,name='confirm'),
    path('Home/',views.home,name='Home'),
    path('Home/Logout/', views.logout_lib,name='Logout'),
]