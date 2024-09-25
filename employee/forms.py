from typing import Any
from django.forms import ModelForm
from django import forms

from user.models import CustomUser
from .models import Employee
from user import validators 


class EmployeeForm(ModelForm):
  class Meta:
    model = Employee
    fields = ['user','first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zip', 'country', 'date_of_birth', 'date_of_joining', 'department', 'designation', 'salary', 'profile_pic']
    
    widgets = {
      'user': forms.Select(attrs={'class': 'form-control'}),
      'first_name': forms.TextInput(attrs={'class': 'form-control'}),
      'last_name': forms.TextInput(attrs={'class': 'form-control'}),
      'email': forms.EmailInput(attrs={'class': 'form-control'}),
      'phone': forms.TextInput(attrs={'class': 'form-control'}),
      'address': forms.TextInput(attrs={'class': 'form-control'}),
      'city': forms.TextInput(attrs={'class': 'form-control'}),
      'state': forms.TextInput(attrs={'class': 'form-control'}),
      'zip': forms.TextInput(attrs={'class': 'form-control'}),
      'country': forms.TextInput(attrs={'class': 'form-control'}),
      'date_of_birth': forms.DateInput(attrs={'class': 'form-control','type':'date'}, format='%Y-%m-%d'),
      'date_of_joining': forms.DateInput(attrs={'class': 'form-control','type':'date'}, format='%Y-%m-%d'),
      'department': forms.TextInput(attrs={'class': 'form-control'}),
      'designation': forms.TextInput(attrs={'class': 'form-control'}),
      'salary': forms.NumberInput(attrs={'class': 'form-control'}),
      'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
    }
    
  def clean(self) -> dict[str, Any]:
    cleaned_data = super().clean()
    if validators.EmailValidator(cleaned_data['email']):
      raise forms.ValidationError('Email is not valid')
    ## add a custom data outside of the form fields
    return cleaned_data
  
  def save(self, commit: bool = ...) -> Any:
    
    return super().save()
  