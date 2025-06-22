from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from videos.views import VideoCreateView, VideoDetailView, VideoListView

urlpatterns = [
    path("", VideoListView.as_view(), name="video-list"),
    path("create/", VideoCreateView.as_view(), name="video-create"),
    path("<slug:slug>/", VideoDetailView.as_view(), name="video-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
