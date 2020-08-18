from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .models import Image
from .serializer import ImageSerializer
from .module import ImageModule

class ImageViews(APIView):

    def get(self, request):
        image = Image.objects.all()
        serializer = ImageSerializer(data=image, many=True)
        if serializer.is_valid():
            print('serializer.data')
        print(serializer.data)
        return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            path = serializer.data['src']
            img = ImageModule(path)

        return Response({}, status=status.HTTP_200_OK)
