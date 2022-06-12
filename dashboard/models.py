from random import choices
from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.

user_choices = [('Doctor' , 'Doctor') , ('Patient' , 'Patient')]
user_status_choices = [('online' , 'online') , ('offline' , 'offline')]
blog_category_choices = [ ("Metal Helth","Metal Helth") , ("Heart Disease","Heart Disease") , ("COVID-19","COVID-19") , ("Immunization","Immunization") ]
blog_status_choices = [ ('Draft' , 'Draft' ) , (  "Uploaded" , "Uploaded" )]

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

class Blog(models.Model):
    blog_id = models.CharField(primary_key= True , max_length= 5  ,null = False )
    user_id = models.ForeignKey(to = User , on_delete= models.CASCADE)
    blog_title = models.CharField(max_length=50 , null = False )
    image_path = models.CharField(max_length=500 , null=True)
    category = models.CharField(max_length=100  , choices= blog_category_choices)
    summary = models.CharField(max_length=300 , null = True )
    content = models.CharField(max_length=2000 ,null = True )
    blog_status = models.CharField(max_length = 50  , choices= blog_status_choices)
    publish_datetime = models.DateTimeField(auto_now_add=True)

