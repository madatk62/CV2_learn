from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:

        model = Image
        fields = ['name', 'src']

# class ImageResultSerializer(serializers.ModelSerializer):
#     imageResult = ser