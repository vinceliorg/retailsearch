from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import sys
from . import searchclient
import json


# Create your views here.
@api_view(['GET'])
def Search(request):
    query = request.query_params.get('query')

    results =  searchclient.search(query)
    res_dict = []
    for result in results:
        res_dict.append(json.loads(result))
    return Response(res_dict)