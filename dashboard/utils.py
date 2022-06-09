from django.conf import settings
from .models import User,Doctor,Paitient
from PIL import Image
import os , json

def generate_user_id(user_type):
    users = len(User.objects.all())+1
    length = len(str(users))
    id = 'P' if user_type == 'Patient' else 'D'
    id += "0"*(4-length)
    id += str(users)

    print(f"generated user id : {id}")

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
    img_path = os.path.join(settings.MEDIA_ROOT,image_url[:-3]+'png')
    img.save(img_path )
    return img_path


    