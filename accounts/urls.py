from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from accounts import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('sms_test/', views.SMSView.as_view(), name="logout")
]


# Authenticate endpoints
urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
