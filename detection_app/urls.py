from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_image, name='upload_image'),
    path('result/<str:filename>/', views.result, name='result'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('add/', views.add_known_face, name='add_known_face'),
    path('success/<str:filename>/<str:person_name>/', views.face_added_success, name='face_added_success'),
]