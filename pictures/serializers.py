from rest_framework import serializers
from .models import Pictures


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = '__all__'