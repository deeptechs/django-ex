from django.urls import path
from accounts.views import LoginView, register_view, logout_view

app_name = 'accounts'

urlpatterns = [

    path('login', LoginView.as_view(), name="login"),
    path('register', register_view, name="register"),
    path('logout', logout_view, name="logout"),

]
