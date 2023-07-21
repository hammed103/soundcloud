from django.urls import path
from . import views
from charts.views import Update,Render


urlpatterns = [
    path("api/update",Update.as_view()),
    path("api/render",Render.as_view())
]
