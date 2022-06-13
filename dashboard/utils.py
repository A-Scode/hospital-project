from django.conf import settings
from .models import User,Doctor,Paitient,Blog
from PIL import Image
import os , json
from cryptography.fernet import Fernet


def generate_user_id(user_type):
    users = len(User.objects.all())+1
    length = len(str(users))
    id = 'P' if user_type == 'Patient' else 'D'
    id += "0"*(4-length)
    id += str(users)

    print(f"generated user id : {id}")

    return id

def generate_blog_id():
    blogs = len(Blog.objects.all())+1
    length = len(str(blogs))
    id = 'B'
    id += "0"*(4-length)
    id += str(blogs)

    print(f"generated blog id : {id}")

    return id

def check_email_exists(email):
    if (len(Doctor.objects.filter(email_id = email)) > 0 or len(Paitient.objects.filter(email_id = email)) > 0 ):
        return True
    else : return False

def check_username_exists(username):
    if (len(Doctor.objects.filter(username = username)) > 0 or len(Paitient.objects.filter(username = username)) > 0 ):
        return True
    else : return False

def get_user_id(username):
    if( len(Doctor.objects.filter(username = username))>0):
        user = Doctor.objects.get(username = username)
        return user.user_id
    elif ( len(Paitient.objects.filter(username = username))>0 ):
        user = Paitient.objects.filter(username = username)
        return user.user_id


def user_data(user_id):
    user = User.objects.get(user_id = user_id)

    if (user["user_type"]== "Doctor"):
        return Doctor.objects.get(usre_id = user_id)
    elif (user["user_type"] == "Patient"):
        return Paitient.objects.get(user_id = user_id)



def compress_image(image_url):
    img = Image.open(os.path.join(settings.MEDIA_ROOT, image_url ))

    width , height = img.size
    
    h,w =0,0
    if (height>width):
        h = 400
        w = int( 400* (width/height))
    else:
        w=400
        h = int(400*(height/width))
    img = img.resize((w,h))
    img_path = image_url[:-3]+'png'

    if (os.path.exists(os.path.join(settings.MEDIA_ROOT, image_url ))): os.remove(os.path.join(settings.MEDIA_ROOT, image_url ))
    img.save(os.path.join(settings.MEDIA_ROOT,img_path ))
    return img_path

def encrypt_pass(password):
    configs = open("configs.json")
    data = json.load(configs)
    f = Fernet(data["fernetKey"])
    enc = f.encrypt(password.encode())
    return enc.decode()

def decrypt_pass(password):
    configs = open("configs.json")
    data = json.load(configs)
    f = Fernet(data["fernetKey"])
    dec = f.decrypt(password.encode())
    return dec.decode()


def get_user_details(user):
    res_data = {}
    res_data['user_id'] = user.user_id.user_id
    res_data['firstname'] = user.first_name
    res_data['lastname'] = user.last_name
    res_data['username'] = user.username
    res_data['profile_picture_path'] = user.profile_picture_path
    res_data['email_id'] = user.email_id
    res_data['address'] = user.address
    res_data['user_type'] = user.user_id.user_type

    return res_data

def get_blog_details(blog):
    res_data = {}
    res_data['user_id'] = blog.user_id.user_id
    res_data['blog_id'] = blog.blog_id
    res_data['blog_title'] = blog.blog_title
    res_data['image_path'] = blog.image_path
    res_data['category'] = blog.category
    res_data['summary'] = blog.summary
    res_data['content'] = blog.content
    res_data['blog_status'] = blog.blog_status
    res_data['publish_datetime'] = blog.publish_datetime.strftime("%d/%m/%Y")

    return res_data


    