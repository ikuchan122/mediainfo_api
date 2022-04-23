from django.urls import path
from mediainfo_api import views

urlpatterns = [
    path("getVideoDimensions", views.getVideoDimensions,
         name="getVideoDimensions"),
]
