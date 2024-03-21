from django.urls import path, include
from post.views.data import PostingView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

   path("posting/", PostingView.as_view()),
   path("posting/<int:pk>/", PostingView.as_view()),
   path("posting/<str:pk>/", PostingView.as_view()),
   path("posting/<slug:pk>/", PostingView.as_view()),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
