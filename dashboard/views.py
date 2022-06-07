from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Create your views here.


#Check for running
@api_view(['GET'])
def hello(request ):
    return JsonResponse({"hello" : "hii"})



