from random import choices
from django.db import models

# Create your models here.

user_choices = [('Doctor' , 'Doctor') , ('Patient' , 'Paitient')]
user_status_choices = [('Doctor' , 'Doctor') , ('Patient' , 'Paitient')]

class User(models.Model): 
    user_id = models.CharField(max_length =5  , primary_key= True , null= False)
    user_type = models.CharField( choices = user_choices , null = False  , max_length=100)
    user_status = models.CharField( choices=user_status_choices , max_length=100  , default=False )

class Doctor(models.Model) :
    user_id = models.ForeignKey( to = User , on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 50 , null = False)
    last_name = models.CharField( max_length = 50 , default="")
    profile_picture_path = models.CharField( max_length = 1000 )
    username = models.CharField( max_length = 50 )
    email_id = models.EmailField(unique= True  , max_length= 100)
    password = models.CharField(max_length=500)
    address = models.CharField(max_length= 500  , null = False)

class Paitient(models.Model) :
    user_id = models.ForeignKey( to = User , on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 50 , null = False)
    last_name = models.CharField( max_length = 50 , default="")
    profile_picture_path = models.CharField( max_length = 1000 )
    username = models.CharField( max_length = 50 )
    email_id = models.EmailField(unique= True  , max_length= 100)
    password = models.CharField(max_length=500)
    address = models.CharField(max_length= 500 )
