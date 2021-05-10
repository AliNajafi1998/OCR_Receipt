import os
from django.conf import settings

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
        # TODO: 'filename' is an entry for detector function
        # TODO: returned json should be used as response
        return Response({'result': 'result'})
