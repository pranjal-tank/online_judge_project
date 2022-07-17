from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from account.forms import Signupform
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django. contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from .tokens import account_activation_token

def register(request):
    if request.method=='POST':
        fm=Signupform(request.POST)
        if fm.is_valid():
          user_email=fm.cleaned_data['email']
          if User.objects.filter(email=user_email).exists():
            messages.error(request,'Email already exist!')
            return render(request,'account/register.html',{'form':fm})
          user = fm.save(commit=False)  
          user.is_active = False  
          user.save() 
          messages.success(request,'Account created successfully! Please verify your email by clicking on the link sent to your email address')
          
          uname=fm.cleaned_data['username']
          current_site=get_current_site(request)
          email_subject="Conform your email!"
          email_message=render_to_string('email_conformation.html',{
            'name':uname,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
          })
          to_email = fm.cleaned_data['email'] 
          email = EmailMessage(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            to=[to_email],
          )
          email.fail_silently=True
          email.send()

          return HttpResponseRedirect(reverse("login"))
    else:
      fm=Signupform()
    return render(request,'account/register.html',{'form':fm})

def user_login(request):
  if not request.user.is_authenticated:
    if request.method == 'POST':
      fm=AuthenticationForm(request=request,data=request.POST)
      if fm.is_valid():
          user_name=fm.cleaned_data['username']
          user_password=fm.cleaned_data['password']
          user=authenticate(username=user_name,password=user_password)
          if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
    else:
      fm=AuthenticationForm()
    return render(request,'account/user_login.html',{'form':fm})
  else:
    return HttpResponseRedirect(reverse("index"))

def activate(request,uidb64,token):
  try:
    uid=force_str(urlsafe_base64_decode(uidb64))
    myuser=User.objects.get(pk=uid)
  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    myuser=None
  
  if myuser is not None and account_activation_token.check_token(myuser,token):
    myuser.is_active=True
    myuser.save()
    login(request,myuser)
    return HttpResponseRedirect(reverse("index"))
  else:
    messages.error(request,'Activation failed, Please try again!')
    return render(request,'account/register.html')



  


