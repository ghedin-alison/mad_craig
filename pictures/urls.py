from django.urls import path
from .views import PicturesViewSet, UserAPIView

urlpatterns = [
    path('pictures', PicturesViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('pictures/<str:pk>', PicturesViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
    path('user', UserAPIView.as_view())]
