from django.urls import path



urlpatterns = [
path('register/',UserRegisterView.as_view(), name='user_register'),

    ]