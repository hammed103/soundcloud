from django.urls import path
from . import views
from charts.views import Update,Render


urlpatterns = [
    path('', views.top_50, name='top_50'),
    path("api/update",Update.as_view()),
    path("api/render",Render.as_view())
]
