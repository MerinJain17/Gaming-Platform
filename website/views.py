
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from game import settings
from website.models import Review

from .tokens import generate_token


# Create your views here.
def index(request):
    return render(request, 'index.html')

def play(request):
    return render(request, 'play.html')


def login(request):
    return render(request, 'login.html')

def random(request):
    return render(request, 'random.html')

def about(request):
    return render(request, 'about.html')

def game1(request):
    return render(request, 'game1.html')

def game2(request):
    return render(request, 'game2.html')

def game3(request):
    return render(request, 'game3.html')

def game4(request):
    return render(request, 'game4.html')

def game5(request):
    return render(request, 'game5.html')

def game6(request):
    return render(request, 'game6.html')
    
def account(request):

#-------------------------------SIGNUP FORM---------------------------
    if request.method=="POST":
        username =request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        phone=request.POST['phone']      
        
#------------------------------------USER CONDITIONS-----------------------
        if User.objects.filter(username=username):
            messages.error(request,"Username already exists!")
            return redirect('account')
        

        if len(username)>15:
            messages.error(request,"User name must not exceed 15 characters!")
            return redirect('account')

        
#        if len(password)>5:
#            messages.error(request,"Password must have 5")
#            return redirect('account')

        if not phone.isdecimal():
            messages.error(request,"only digits can be used!")
            return redirect('account')

        if not username.isalnum():
            messages.error(request,"only digits and alphabets can be used in user name!")
            return redirect('account')

        myuser = User.objects.create_user(username,email,password)
        myuser.ph=phone
        myuser.is_active = False
        myuser.save()
        
        messages.success(request,"Your Account has been successfully created.")


#-------------------------------------EMAIL MESSAGE------------------------

#====================================welcome email================================

        subject="Welcome to our website DASHLANE!"
        message="Hello\t" +  myuser.username + "\n we are so happy to have you,as a new member of the family.we hope yoy have a great time enjoy ! \n we have sent you an email for confirmation please click the link in order to activate your account\n http://127.0.0.1:8000/login \n\nThankyou"
        from_email= settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

#====================================confirm email==================================
        current_site = get_current_site(request)
        email_subject="Confirm your email!"
        message2=render_to_string('email_confirmation.html',{
            "name":myuser.username,
            "domain":current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser) ,
         })
        email=EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [myuser.email]
        )
        email.fail_silently = True
        email.send()
        return redirect('account')

    return render(request, 'account.html')


def contact(request):
    if request.method=="POST":
        feedback=request.POST.get('feedback')
        desc=request.POST.get('desc')
        review=Review(feedback= feedback,desc=desc,date=datetime.today())
        review.save()
    
    return render(request, 'contact.html')


def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        #login(request,myuser)
        return redirect('login')

    else:
        return render(request, "activation_fail.html")
    
def activation_fail(request):
    return render(request, 'activation_fail.html')
    
