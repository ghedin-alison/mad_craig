from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Pictures, User
from .serializers import PictureSerializer
import random


# Create your views here.
class PicturesViewSet(viewsets.ViewSet):
    def list(self, request):  # /api/pictures(get request)
        pictures = Pictures.objects.all()
        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data)

    def create(self, request):  # /api/pictures(post request)
        serializer = PictureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):  # /api/pictures/<str:id>
        picture = Pictures.objects.get(id=pk)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)

    def update(self, request, pk=None):  # /api/pictures/<str:id>
        picture = Pictures.objects.get(id=pk)
        serializer = PictureSerializer(instance=picture, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):  # /api/pictures/<str:id>
        picture = Pictures.objects.get(id=pk)
        picture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            "id": user.id
        })


