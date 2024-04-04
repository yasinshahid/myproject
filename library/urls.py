from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('create/', views.book_create, name='book_create'),
    path('book_edit/<int:pk>/', views.book_edit, name='book_edit'),
    path('book_delete/<int:pk>/', views.book_delete, name='book_delete'),
    path('list/', views.book_list, name='book_list'),
]
