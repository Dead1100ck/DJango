from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', RegisterPage.as_view(), name='register_page'),
    path('login/', LoginPage.as_view(), name='login_page'),
    path('account/', account_page, name='user_account_page'),
    path('logout/', user_logout, name='user_logout'),

    # path('clients/', clients),
    path('comments/', comments, name='comments_page'),
    path('contacts/', contacts, name='contacts_page'),
    # path('teams/', teams),
    # path('projects/', projects),
    # path('employees/', employees)
]