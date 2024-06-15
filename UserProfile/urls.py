from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', views.signin, name='login'),
    path('register/', views.user_register, name='register'),
    path('user/change-password/', views.change_password, name='change_password'),
    path('user/details/<int:id>', views.user_detail, name='user_details'),
    path('user/update/<int:id>', views.user_update, name='user_update'),
    path('user/myorders', views.my_orders, name='my_orders'),
    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('enable-totp/', views.enable_totp, name='enable_totp'),
    path('verify-totp/', views.verify_totp, name='verify_totp'),
]
