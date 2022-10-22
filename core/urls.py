# core/urls.py

# django
from django.urls import path

# local
from . import views

app_name = "core"

urlpatterns = [
	path("", views.HomeView.as_view(), name="home"),
]