from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', hello),
    path('username_exists' , username_exists),
    path('email_exists' , email_exists),
    path('signup' , signup),
    path('login' , login),
    path('get_user_details' , get_user_details),
    path('logout' , logout),
    path('check_drafts' , check_drafts),
    path('draft_blog' , draft_blog),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


