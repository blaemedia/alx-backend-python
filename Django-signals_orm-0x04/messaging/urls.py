# messaging/urls.py
from django.urls import path,include
from .views import delete_user

urlpatterns = [
    path("delete-account/", delete_user, name="delete_user"),
    path("messaging/", include("messaging.urls")),
]