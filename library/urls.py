from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_user, name='account_login'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('accounts/login/', views.login_user, name='account_login'),
    path('create/', views.book_create, name='book_create'),
    path('book_edit/<int:pk>/', views.book_edit, name='book_edit'),
    path('book_delete/<int:pk>/', views.book_delete, name='book_delete'),
    path('list/', views.book_list, name='book_list'),
    path('logout/', views.logout_user, name='logout_user'),
]
