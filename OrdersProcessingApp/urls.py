from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home_page'),
    path('account/', account_page, name='user_account_page'),
    path('register/', RegisterPage.as_view(), name='register_page'),
    path('login/', LoginPage.as_view(), name='login_page'),
    path('logout/', user_logout, name='user_logout'),

    path('addcomment/', AddComment.as_view(), name='add_comment_page'),
    path('comments/', comments, name='comments_page'),

    path('orders/', orders_page, name='employee_orders'),
    path('takeorder/<int:id_order>', take_order, name='take_order'),
]