from django.shortcuts import redirect, render
from django.views.generic import View
from .forms import LoginForm, SignupForm
from django.contrib import messages
from django.contrib.auth import  login, logout
from group.permissions import has_permission
from django.contrib.auth.decorators import login_required
from group.models import CustomGroup , Module
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
@login_required(login_url='user:user_login')
# @has_permission('User','view')
def index(request):
    context = {
        'title': f'Home | {request.user.username}',
        'url_pattern': 'user:index',
        'link_name': 'Home',
        "button_name": 'Edit Profile',
        "button_link": 'user:edit_profile'
    }
    return render(request, 'index.html', context = context)

class UserEditProfileView(LoginRequiredMixin,View):
    
    def get(self, request):
        context = {
            'title': f'Edit Profile | {request.user.username}',
            'url_pattern': 'user:edit_profile',
            'link_name': 'Edit Profile',
            "button_name": 'Update Profile',
        }
        return render(request, 'user/edit-profile.html', context = context)
    
    def post(self, request):
        form = UserEditForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('user:index')
        messages.error(request, form.errors,extra_tags='danger')
        return redirect('user:edit_profile')

class UserSignupView(View):
    def set_user_guest(self):
        user = self.request.user
        group,created = CustomGroup.objects.get_or_create(name='Guest')
        if not created:
            group.user.add(user)
            group.save()
            return
        
        group = CustomGroup.objects.create(name = 'Guest')
        module_names = ['User','Group','Permission','Employees']
        modules = []
        for module_name in module_names:
            module = Module.objects.create(name = module_name)
            module.save()
            modules.append(module)
        
        group.module.set(modules)
        group.user.add(user)
        group.save()
        return 
    
    def get(self, request):
        if request.user.is_authenticated:
            context ={
                'message': 'You are already logged in',
                'tags': 'info'
            }
            messages.info(request, 'You are already logged in')
            return redirect('user:index', context = context)
        return render(request, 'user/signup.html', context = {'title': 'Signup'})
    
    def post(self, request):
      with transaction.atomic():    
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            self.set_user_guest()
            return redirect('user:index')
        print(form.errors)
        messages.error(request, form.errors,extra_tags='danger')
        return redirect('user:user_signup')

class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in')
            return redirect('user:index')
        return render(request, 'user/login.html', context = {'title': 'Login'})
  
    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Invalid Data found')
            return redirect('user:user_login')
        user = form.save()
        if user.is_authenticated:
            login(request,user)
            messages.success(request, 'Login successful')
            return redirect('user:index')
        messages.error(request, 'Invalid credentials',extra_tags='danger')
        return redirect('user:user_login')


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('user:user_login')
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('user:user_login')
        
        