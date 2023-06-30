from django.urls import path
from . import views

app_name = "MiBarrioApp"

urlpatterns = [
    path('', views.homepage, name="homepage"),
]
