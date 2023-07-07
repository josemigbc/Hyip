from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from .views import RegisterUserView

urlpatterns = [
    path('login/',LoginView.as_view(template_name="authentication/login.html")),
    path("signup/", RegisterUserView.as_view(), name=""),
    path("signup/<int:pk>/", RegisterUserView.as_view(), name=""),
    path('logout/',LogoutView.as_view(),name="logout"),
]
