from .models import User,Doctor,Paitient

def generate_user_id(user_type):
    users = len(User.objects.all())
    id = 'P' if user_type == 'Patient' else 'D'
    id+= usres+1

    return id

def check_mail_exists(email):
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
    elif (user["user_type"] == "Paitient" or user["user_type"] == "Patient"):
        return Paitient.objects.get(user_id = user_id)


    