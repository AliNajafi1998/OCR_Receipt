import os
import json
from django.conf import settings

from utils.ocr_scanner import detect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import MultiPartParser


class PredictorView(APIView):
    parser_classes = [MultiPartParser]
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        file_content = request.data.get('file')
        media = f"{str(settings.BASE_DIR).replace('/src', '')}/media"
        filename = f'{media}/{file_content._name}'
        if not os.path.isdir(media):
            os.mkdir(media)
        with open(filename, 'wb+') as temp_file:
            for chunk in file_content.chunks():
                temp_file.write(chunk)
        print(filename)
        result = detect(filename)
        print(result)
        return Response({'result': json.loads(result)})
