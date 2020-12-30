from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class DishForm(ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'
        exclude = ['Total_Sold', 'Offer']
        widgets = {
            'Dish_Name' : forms.TextInput(attrs={'class': 'form-control'}),
            'Dish_Discription' : forms.TextInput(attrs={'class': 'form-control'}),
            'Dish_Type' : forms.Select(attrs={'class': 'form-control'}),
            'Price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'Offer' : forms.NumberInput(attrs={'class': 'form-control'}),
            #'Dish_File_Path' : forms.ImageInput(attrs={'class': 'form-control'}),
        }

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['Address', 'Ph_no']
        widgets = {
            'Address' : forms.TextInput(attrs={'class': 'form-control'}),
            'Ph_no' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContactForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['Address', 'Ph_no', 'E_Mail']
        widgets = {
            'Address' : forms.TextInput(attrs={'class': 'form-control'}),
            'Ph_no' : forms.TextInput(attrs={'class': 'form-control'}),
            'E_Mail' : forms.EmailInput(attrs={'class': 'form-control'}),
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']