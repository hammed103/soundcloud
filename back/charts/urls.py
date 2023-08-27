from django.urls import path
from . import views
from charts.views import Update, Render, tik, tiktok_view,Discover,RenderDiscovery,request_form_view
from django.urls import path
from .new_views import download_file ,Updatefire




urlpatterns = [
    path("api/tiktok", tiktok_view, name="tiktok"),
    path("api/update", Update.as_view()),
    path("api/discover", Discover.as_view()),
    path("api/render", Render.as_view()),
     path("api/render2", RenderDiscovery.as_view()),
    path("api/tik", tik.as_view()),
    path('api/request_form', request_form_view, name='request_form'),
    path('api/download/', download_file, name='download_file'),
    path("api/updatefire", Updatefire.as_view()),

]
