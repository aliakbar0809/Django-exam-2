from django import forms
from .models import *

# Form user
class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):

    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)



class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['photo', 'bio']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'image']
