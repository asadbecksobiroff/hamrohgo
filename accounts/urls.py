from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_telegram, name='auth_telegram'),
    path('auth/login/', views.auth_telegram_login, name='auth_telegram_login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/change-status/<int:pk>/', views.ChangeUserRoleView.as_view(), name='change_role'),
    path('profile/car/create/', views.CarCreateView.as_view(), name='car_create'),
    path('profile/car/update/<int:pk>/', views.CarUpdateView.as_view(), name='car_update'),
    path('profile/car/delete/<int:pk>/', views.CarDeleteView.as_view(), name='car_delete'),
]