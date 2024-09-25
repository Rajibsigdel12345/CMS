from typing import Any
from django.forms import ModelForm
from django import forms
from django.db.models import Q 
from django.contrib.auth.models import AnonymousUser
from user import validators
from .models import CustomUser
from django.contrib.auth import authenticate

class SignupForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class UserEditForm(ModelForm):
    
    class Meta:
        model = CustomUser
        fields = "__all__"
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(required=False, max_length=100, error_messages={'message': 'Username is required'})
    password = forms.CharField(widget=forms.PasswordInput(),error_messages={'message': 'Password is required'})
    email = forms.EmailField(required=False, validators=[validators.EmailValidator], error_messages={'message': 'Email is required'})
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        
        
        if len(username)<=0 and len(email)<=0:
            raise forms.ValidationError('Either username or email is required')
        
        return cleaned_data
    
    def save(self):
        user = CustomUser.objects.filter(Q(username=self.cleaned_data['username'])|Q(email=self.cleaned_data['username']))
        authenticate(user)
        if user.exists() and user.first().check_password(self.cleaned_data['password']):
            return user.first()
        return AnonymousUser()
        
    