from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView,
    UserFollowView,
    UserUnfollowView,
    EditUserView,
)

app_name = "account"
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path("profile/<int:user_id>/", UserProfileView.as_view(), name="user_profile"),
    path("reset/", UserPasswordResetView.as_view(), name="reset_password"),
    path(
        "reset/done/", UserPasswordResetDoneView.as_view(), name="password_reset_done"
    ),
    path(
        "confirm/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "confirm/complete",
        UserPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("follow/<int:user_id>/", UserFollowView.as_view(), name="user_follow"),
    path("unfollow/<int:user_id>/", UserUnfollowView.as_view(), name="user_unfollow"),
    path("edit_user/", EditUserView.as_view(), name="edit_user"),
]
