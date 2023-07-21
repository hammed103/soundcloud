from django.urls import path
from . import views
from charts.views import Update,Render,tik,tiktok_view


urlpatterns = [

    path('', views.top_50, name='top_50'),
    path('/tiktok', tiktok_view, name='tiktok'),
    path("api/update",Update.as_view()),
    path("api/render",Render.as_view()),
     path("api/tik",tik.as_view())
]
