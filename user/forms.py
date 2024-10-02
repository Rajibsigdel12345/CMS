
from typing import Any
from django.forms import ModelForm
from django import forms
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from user import validators
from .models import CustomUser
from django.contrib.auth import authenticate, login
from group.models import CustomGroup


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


class UserAddFrom(ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=CustomGroup.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name',
                  'email', 'date_joined', 'groups',]
        attrs = {'class': 'form-control'}
        widgets = {
            'username': forms.TextInput(attrs=attrs),
            'first_name': forms.TextInput(attrs=attrs),
            'last_name': forms.TextInput(attrs=attrs),
            'email': forms.EmailInput(attrs=attrs),
            # 'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'date_joined': forms.DateInput(attrs={'type':'date',**attrs}, format='%Y-%m-%d'),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit: bool = ...) -> Any:
        user = super().save(commit=False)
        user.set_unusable_password()
        user.save()
        user.customgroup_set.add(*self.cleaned_data['groups'])
        return user


class ProfileEditForm(ModelForm):
    attrs = {'class': 'form-control'}
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs), required=True)
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs), required=False)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs), required=False)

    def is_valid(self):
        valid = super().is_valid()
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        old_password = self.cleaned_data.get('current_password')
        if len(new_password) > 0:

            if len(new_password) < 8:
                self.add_error(
                    'new_password', 'Password should be atleast 8 characters')
                valid = False

            if not confirm_password:
                self.add_error('confirm_password',
                               'Confirm password is required')
                valid = False

            if new_password != confirm_password:
                self.add_error(
                    'new_password', 'New password and confirm password should be same')
                valid = False

        if not self.instance.check_password(old_password):
            self.add_error('current_password', 'Current password is incorrect')
            valid = False
        print(valid)
        return valid

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email',
                  'profile_pic', 'current_password', 'new_password', 'confirm_password']
        class_attr = {
            'class': 'form-control'
        }
        widgets = {
            'username': forms.TextInput(attrs=class_attr),
            'first_name': forms.TextInput(attrs=class_attr),
            'last_name': forms.TextInput(attrs=class_attr),
            'email': forms.EmailInput(attrs=class_attr),
            'profile_pic': forms.FileInput(attrs={'accept': "image/png,image/jpeg,image/jpg", **class_attr}),
            'current_password': forms.PasswordInput(attrs=class_attr),
            'new_password': forms.PasswordInput(attrs=class_attr),
            'confirm_password': forms.PasswordInput(attrs=class_attr),
            'groups': forms.SelectMultiple(attrs=class_attr),
        }

    def save(self, commit=True):
        # Automatically handles file saving if commit=True
        user = super().save(commit=False)  # Don't save to the database just yet
        print(self.cleaned_data.get('profile_pic'))
        # If there's a file in the cleaned_data
        if self.cleaned_data.get('profile_pic'):
            user.profile_pic = self.cleaned_data['profile_pic']
        if self.cleaned_data.get('new_password'):
            user.set_password(self.cleaned_data['new_password'])

        if commit:
            user.save()  # Save the instance to the database
        return user


class LoginForm(forms.Form):
    username = forms.CharField(required=False, max_length=100, error_messages={
                               'message': 'Username is required'})
    password = forms.CharField(widget=forms.PasswordInput(), error_messages={
                               'message': 'Password is required'}, required=False)
    email = forms.EmailField(required=False, validators=[
                             validators.EmailValidator], error_messages={'message': 'Email is required'})

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if len(username) <= 0 and len(email) <= 0:
            raise forms.ValidationError('Either username or email is required')

        return cleaned_data

    def save(self):
        user = CustomUser.objects.filter(Q(username=self.cleaned_data['username']) | Q(
            email=self.cleaned_data['username']))
        
        if user.exists():
            user = user.first()
            if user.has_usable_password() and user.check_password(self.cleaned_data['password']):
                return user
            if not user.has_usable_password():
                return user, False
        return AnonymousUser()

class ChangePasswordForm(ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = CustomUser
        fields = ['new_password', 'confirm_password']
        widgets = {
            'new_password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }
        
    def is_valid(self):
        valid = super().is_valid()
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if len(new_password) < 8:
            self.add_error('new_password', 'Password should be atleast 8 characters')
            valid = False
        if new_password != confirm_password:
            self.add_error('new_password', 'New password and confirm password should be same')
            valid = False
        return valid
    
    def save(self, commit: bool = ...) -> Any:
        self.instance.set_password(self.cleaned_data['new_password'])
        self.instance.save()
        return self.instance
