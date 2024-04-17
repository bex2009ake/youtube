from django.urls import path
from app.views import *

urlpatterns = [
    path('singup/', Singup.as_view(), name='singup'),
    path('singin/', Singin.as_view(), name='singin'),
    path('video/', VideoCreateRead.as_view(), name='video'),
    path('video/<int:pk>/', DeleteVideo.as_view(), name='delete'),
    path('like/<int:pk>/', LikesViewsVideo.as_view(), name='like'),
    path('comment/<int:pk>/', CommentCreateRead.as_view(), name='comment'),
    path('favorite/', FavoriteRead.as_view(), name='favorites'),
    path('favorite/<int:pk>', FavoriteCreateRead.as_view(), name='favorite'),
    path('history/', HistoryRead.as_view(), name='histories'),
    path('history/<int:pk>', HistoryCreateRead.as_view(), name='history'),
]
