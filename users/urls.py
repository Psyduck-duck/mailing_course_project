from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy
from . import views

from users.apps import UsersConfig
# from users.views import (UserCreateView, UserListView, UserUpdateView,
#                          email_verification, view_profile)

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('<int:pk>', views.UserDetailView.as_view(), name='user_info'),
    # path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    # path("update/<int:pk>/", UserUpdateView.as_view(), name="user_detail"),
    # path("profile/", view_profile, name="profile"),
    # path(
    #     "password-reset/",
    #     PasswordResetView.as_view(
    #         template_name="users/password_reset_form.html",
    #         email_template_name="users/password_reset_email.html",
    #         success_url=reverse_lazy("users:password_reset_done"),
    #     ),
    #     name="password_reset",
    # ),
    # path(
    #     "password-reset/done/",
    #     PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
    #     name="password_reset_done",
    # ),
    # path(
    #     "password-reset/<uidb64>/<token>/",
    #     PasswordResetConfirmView.as_view(
    #         template_name="users/password_reset_confirm.html",
    #         success_url=reverse_lazy(
    #             "users:password_reset_complete",
    #         ),
    #     ),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "password-reset/complete/",
    #     PasswordResetCompleteView.as_view(
    #         template_name="users/password_reset_complete.html"
    #     ),
    #     name="password_reset_complete",
    # ),
    # path("user/list", UserListView.as_view(), name="user_list"),
    # path("user/<int:pk>/block/", UserUpdateView.block_user, name="block_user"),
]
