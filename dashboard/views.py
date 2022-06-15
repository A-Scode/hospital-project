from datetime import datetime
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


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self , name , max_length):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT , name))
        return name


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
            fs = OverwriteStorage()
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

    except Exception as e:
        print(e)
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
    data = json.loads(request.POST['data'])

    blog_id = None
    blog = None
    img_path = ""
    user = User.objects.get(user_id = data['user_id'])
    exsist  = None;

    if('blog_id' in data.keys()):
        blog_id = data['blog_id']
        exsist = True
        
    else:
        blog_id = utils.generate_blog_id()
        exsist = False

            
    
    if( len(request.FILES)>0):
        filename = os.path.join('blog_title_imgs/',blog_id +request.FILES['blog_title_imgae'].name[-4:])
        if (os.path.exists(filename)): os.remove(filename)
        fs = OverwriteStorage()
        file = request.FILES['blog_title_imgae']
        print(request.FILES['blog_title_imgae'])
        fs.save( filename , file)
        
        utils.compress_image(filename)
        img_path = "blog_title_imgs/"+blog_id+".png"
    else:
        img_path = "blog_title_imgs/"+blog_id+".png"

    
    print(img_path)

        
    if exsist:
        blog = Blog.objects.get(blog_id = blog_id)

        blog.blog_id  = blog_id
        blog.user_id  = user
        blog.blog_title  = data['blog_title']
        blog.image_path  = img_path
        blog.category  = data['category']
        blog.summary  = data['summary']
        blog.content  = data['content']
        blog.blog_status  = data['type']
        blog.publish_datetime = datetime.now()

        blog.save()
    else : 
        blog = Blog(
        blog_id = blog_id,
        user_id = user,
        blog_title = data['blog_title'],
        image_path = img_path,
        category = data['category'],
        summary = data['summary'],
        content = data['content'],
        blog_status = data['type'],
        publish_datetime= datetime.now(),
        )

        blog.save()




    return JsonResponse({'status' : "success"})


@api_view(['POST'])
@csrf_exempt
def get_blog_data(request):
    try:
        blog_id = request.headers['blog-id']

        blog = Blog.objects.get(blog_id = blog_id)

        data = utils.get_blog_details(blog)

        return JsonResponse({"status" : "success" , "data" : data})
    except:
        return JsonResponse({"status" : "fail" })

@api_view(['POST'])
@csrf_exempt
def blog_by_category(request):
    mental_health , heart_disease , covid19 , immunization = [],[],[],[]

    blogs = Blog.objects.filter(blog_status = "Uploaded")

    for blog in blogs:
        res = utils.get_blog_details(blog)
        if (blog.category == "Metal Helth"): mental_health.append(res)
        elif (blog.category == "Heart Disease") : heart_disease.append(res)
        elif (blog.category == "COVID-19") : covid19.append(res)
        elif (blog.category == "Immunization") : immunization.append(res)
    
    return JsonResponse({ "status" : "success" , "data":{
        "mental_health":mental_health,
        "heart_disease":heart_disease,
        "covid19":covid19,
        "immunization":immunization
    }})

@api_view(['POST'])
@csrf_exempt
def doctor_list(request):
    res_list = []
    doctors = Doctor.objects.all()

    for doctor in doctors:
        details = utils.get_user_details(doctor)
        res_list.append(details)

    return JsonResponse({'status' : 'success' , 'doc_list' : res_list})



