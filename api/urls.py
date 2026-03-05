from django.urls import path

from api.views.account_view import api_register, api_login, api_logout, AccountView, me, AccountDetailsView
from api.views.posts_view import PostsDetailView, PostsListCreateView

urlpatterns = [
    path('api/account/register', api_register, name='register'),
    path('api/account/login', api_login, name="login"),
    path('api/account/logout', api_logout, name="logout"),
    path('api/account/me', me, name="me"),
    path('api/account/', AccountView.as_view()),
    path('api/account/<int:pk>', AccountDetailsView.as_view()),
    path('api/posts/', PostsListCreateView.as_view()),
    path('api/posts/<int:pk>', PostsDetailView.as_view()),
]