from rest_framework.response import Response
from rest_framework.decorators import api_view
import sys
from api.apputil.ver2 import getnextlesson
# Create your views here.

@api_view(['POST'])
def getData(request):
    print()
    response = getnextlesson.getnextlesson(request.data.get("name"))
    return Response(response)