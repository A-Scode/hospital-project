from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json,os
from . import utils
from dashboard.models import User , Doctor , Paitient
from django.core.files.storage import FileSystemStorage


# Create your views here.


#Check for running
@api_view(['GET'])
def hello(request ):
    return JsonResponse({"hello" : "hii"})

@api_view(['GET','POST'])
@csrf_exempt
def username_exists(request):
    print(request.headers['data'])
    data  = json.loads(request.headers['data'])

    if(utils.check_username_exists(data['username'])):
        return JsonResponse({"username_exists" : True})
    else:
        return JsonResponse({"username_exists" : False})


@api_view(['GET','POST'])
@csrf_exempt
def email_exists(request):
    print(request.headers['data'])
    data  = json.loads(request.headers['data'])

    if(utils.check_email_exists(data['email'])):
        return JsonResponse({"email_exists" : True})
    else:
        return JsonResponse({"email_exists" : False})


@api_view(['POST'])
@csrf_exempt
def signup(request):
    data  = json.loads(request.headers['data'])
    #saving profile photo

    user_id = utils.generate_user_id(data['user_type'])

    if( len(request.FILES)>0):
        fs = FileSystemStorage()
        file = request.FILES['profile_photo']
        print(request.FILES['profile_photo'])
        filename = os.path.join('profile_photos/',user_id +request.FILES['profile_photo'].name[-4:])
        fs.save( filename , file)
        
        img_path = utils.compress_image(filename)

    user = User(user_id  = user_id , user_type = data['user_type'] , user_status = "offline")
    user.save()

    if (data['user_type'] == 'Doctor'):
        user = Doctor(
            user_id = user_id,
            first_name = data['firstname'],
            last_name = data['lastname'],
            profile_picture_path = img_path, 
            username = data['username'],
            email_id = data['email'],
            password = utils.encrypt_pass(data['password']),
            address = data['address']
        )
        user.save()
    else : 
        user = Paitient(
            user_id = user_id,
            first_name = data['firstname'],
            last_name = data['lastname'],
            profile_picture_path = img_path, 
            username = data['username'],
            email_id = data['email'],
            password = utils.encrypt_pass(data['password']),
            address = data['address']
        )
        user.save()
        

        
    


    





