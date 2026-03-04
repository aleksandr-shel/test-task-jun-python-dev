from django.urls import path

from api.views.account_view import api_register, api_login, api_logout, AccountView, me, AccountDetailsView
from api.views.orders_view import OrdersDetailView, OrdersListCreateView

urlpatterns = [
    path('api/account/register', api_register, name='register'),
    path('api/account/login', api_login, name="login"),
    path('api/account/logout', api_logout, name="logout"),
    path('api/account/me', me, name="me"),
    path('api/account/', AccountView.as_view()),
    path('api/account/<int:pk>', AccountDetailsView.as_view()),
    path('api/orders/', OrdersListCreateView.as_view()),
    path('api/orders/<int:pk>', OrdersDetailView.as_view()),
]