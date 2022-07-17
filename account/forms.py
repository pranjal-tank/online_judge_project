import email
from enum import unique
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class Signupform(UserCreationForm):
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={"placeholder":"Email","id":"email"})) 
    class Meta:
       model=User
       fields = ('username','email','password1' ,'password2')



     
