from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json,os
from . import utils
from dashboard.models import User , Doctor , Paitient , Blog
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
    try:

        data  = json.loads(request.headers['data'])
        #saving profile photo

        user_id = utils.generate_user_id(data['user_type'])


        user = User(user_id  = user_id , user_type = data['user_type'] , user_status = "offline")
        user.save()

        if (data['user_type'] == 'Doctor'):
            type_user = Doctor(
                user_id = user,
                first_name = data['firstname'],
                last_name = data['lastname'],
                profile_picture_path = 'profile_photos/'+user_id +request.FILES['profile_photo'].name[-4:], 
                username = data['username'],
                email_id = data['email'],
                password = utils.encrypt_pass(data['password']),
                address = data['address']
            )
            type_user.save()
        else : 
            type_user = Paitient(
                user_id = user,
                first_name = data['firstname'],
                last_name = data['lastname'],
                profile_picture_path = 'profile_photos/'+user_id +request.FILES['profile_photo'].name[-4:], 
                username = data['username'],
                email_id = data['email'],
                password = utils.encrypt_pass(data['password']),
                address = data['address']
            )
            type_user.save()


        if( len(request.FILES)>0):
            fs = FileSystemStorage()
            file = request.FILES['profile_photo']
            print(request.FILES['profile_photo'])
            filename = os.path.join('profile_photos/',user_id +request.FILES['profile_photo'].name[-4:])
            fs.save( filename , file)
            
            img_path = utils.compress_image(filename)
        return JsonResponse({'status':True})
    except:
        return JsonResponse({'status':False})


@api_view(['POST'])
@csrf_exempt
def login(request):
    try:
        data = json.loads(request.headers['data'])

        res_data = {}
        if (utils.check_username_exists(data['username'])):
            print(data)
            if (data['user_type'] == 'Doctor' ):
                user = Doctor.objects.get(username = data['username'])
            else:
                user = Paitient.objects.get(username = data['username'])
            
            if (data['password'] == utils.decrypt_pass(user.password)):

                res_data = utils.get_user_details(user)
                
                log_user = User.objects.get(user_id = user.user_id.user_id)
                log_user.user_status = "online"
                log_user.save()

                return JsonResponse({'status' : "success" , 'data' : res_data}) 
            else:
                return JsonResponse({'status' : "invalid Password"})
            
        else:
            return JsonResponse({'status' : "invalid Username"})

    except:
        return JsonResponse({'status' : "error occured or invalid user type"})



@api_view(['POST'])
@csrf_exempt
def get_user_details(request):

    try:
    
        user = User.objects.get(user_id = json.loads( request.headers['userid']))
        
        if (user.user_type == "Doctor"):
            type_user = Doctor.objects.get(user_id = user)
        else :
            type_user = Paitient.objects.get(user_id = user)

        res_data = utils.get_user_details(type_user)

        return JsonResponse({"status" :"success" , "data" : json.dumps(res_data)})
    except:
        return JsonResponse({"status" :"fail" })


@api_view(['POST'])
@csrf_exempt
def logout(request):
    print(request.headers)
    user_id = json.loads(request.headers['user_id'])
    User.objects.filter(user_id = user_id).update(user_status = "offline")

    return JsonResponse({"status" : "success"})

@api_view(['POST'])
@csrf_exempt
def check_drafts(request):
    data = json.loads(request.headers['user_id'])

    blogs = Blog.objects.filter(user_id = data)

    draft_blogs = [];

    for blog in blogs:
        if(blog.blog_status == "Draft"):
            draft_blogs.append( blog.blog_id)
    return JsonResponse({ "status" : "success" , "data" : draft_blogs })

@api_view(['POST'])
@csrf_exempt
def draft_blog(request):
    data = json.loads(request.headers['data'])

    if('blog_id' in data.keys()):
        Blog.objects.filter(blog_id = data['blog_id']).update(
            blog_title = data['blog_title'],
        )

    
    

        

        
    


    





