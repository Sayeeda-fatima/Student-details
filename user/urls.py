"""All user & auth related endpionts goes here"""

from django.urls import path, include
from user.views.auth import TokenView
from user.views.auth import UserSignupView
from user.views.auth import UserModelListView



urlpatterns = [
    path('', UserModelListView.as_view()),
    path("signup/", UserSignupView.as_view()),
    path("login/", TokenView.as_view()),
]


