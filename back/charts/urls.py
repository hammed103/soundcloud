from django.urls import path
from . import views
from charts.views import Update,Render,tik


urlpatterns = [
    path("api/update",Update.as_view()),
    path("api/render",Render.as_view()),
     path("api/tik",tik.as_view())
]
