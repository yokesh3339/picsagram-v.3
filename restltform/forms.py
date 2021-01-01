from django import forms
from .models import People,follow
from django.contrib.auth.models import User,auth
from cloudinary.forms import CloudinaryJsFileField
class PeopleForm(forms.ModelForm):
    username = forms.CharField(
    widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model=People
        profile=CloudinaryJsFileField()
        fields=[
            'username',
            'description',
            'profile'
        ]
    #def clean_username(self,*args,**kwargs):
     #   username=self.cleaned_data.get("username")
      #  if not username in People.objects.get(id=1).get_username():
       #     raise forms.ValidationError("Logedin as your login or sign up")
        #return username
class UserCreate(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={"required":True}))
    class Meta:
        model=User
        fields=[
            'username',
            'password',
            'first_name',
            'last_name',
            'email',

            ]
    def clean_email(self,*args,**kwargs):
        email=self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken")
        return email

class UserProfile(forms.ModelForm):
    class Meta:
        model=follow
        profile=CloudinaryJsFileField()
        fields=[
            'profile',
            'description'
        ]
class loginform(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
        "placeholders":"Enter Username"
    }))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"required":True}))
    def clean_username(self,*args,**kwargs):
        username=self.cleaned_data.get("username")
        if not username in People.objects.all()[0].get_username():
            raise forms.ValidationError("Invalid username or password")
        return username
    
