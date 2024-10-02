from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from group import choices
from .forms import LoginForm, SignupForm, ProfileEditForm, UserAddFrom, ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import login, logout
from group.permissions import has_permission, has_permission_class
from django.contrib.auth.decorators import login_required
from group.models import CustomGroup, Module
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
# Create your views here.


@login_required(login_url='user:user_login')
# @has_permission('User','view')
def index(request):
    print(request.user.profile_pic)
    context = {
        'title': f'Home | {request.user.username}',
        'url_pattern': 'user:index',
        'link_name': 'Home',
        "button_name": 'Edit Profile',
        "button_link": 'user:user_edit'
    }
    return render(request, 'index.html', context=context)


class UserEditProfileView(LoginRequiredMixin, View):
    login_url = 'user:user_login'

    def get(self, request):
        context = request.session.get('context', {})
        context.update({
            'title': f'Edit Profile | {request.user.username}',
            'url_pattern': 'user:index',
            'link_name': 'Edit Profile',
            "button_name": 'Update Profile',
            "button_link": 'user:user_edit',
            'form': ProfileEditForm(instance=request.user) if 'form' not in context else context['form']
        })
        return render(request, 'user/edit-profile.html', context=context)

    def post(self, request):
        form = ProfileEditForm(
            request.POST, request.FILES, instance=request.user)
        print(request.FILES)
        if form.is_valid():
            form.save()
            login(request, request.user)
            messages.success(request, 'Profile updated successfully')
            return redirect('user:user_edit')
        messages.error(request, 'Invalid data found', extra_tags='danger')
        return redirect('user:user_edit')


class UserSignupView(View):
    def set_user_guest(self):
        user = self.request.user
        group, created = CustomGroup.objects.get_or_create(name='Guest')
        if not created:
            group.user.add(user)
            group.save()
            return

        module_names = ['User', 'Group', 'Permission', 'Employees']
        modules = []
        for module_name in module_names:
            module = Module.objects.create(name=module_name)
            module.save()
            modules.append(module)

        group.module.set(modules)
        group.user.add(user)
        group.save()

    def get(self, request):
        if request.user.is_authenticated:
            context = {
                'message': 'You are already logged in',
                'tags': 'info'
            }
            messages.info(request, 'You are already logged in')
            return redirect('user:index', context=context)
        return render(request, 'user/signup.html', context={'title': 'Signup'})

    def post(self, request):
        with transaction.atomic():
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                self.set_user_guest()
                return redirect('user:index')
            print(form.errors)
            messages.error(request, form.errors, extra_tags='danger')
            return redirect('user:user_signup')

class UserChangePasswordView(View):
    def get(self, request):
        user = CustomUser.objects.filter(pk=request.session.get('context', {}).get('user_id'))
        if not user.exists():
            return redirect('user:user_login')
        context = {
            'title': f'Change Password | {user.first().username}',
            'url_pattern': 'user:index',
            'link_name': 'Change Password',
            "button_name": 'Change Password',
            "button_link": 'user:user_change_password',
        }
        return render(request, 'user/change-password.html', context=context)
    
    def post (self, request):
        user = CustomUser.objects.filter(pk=request.session.get('context', {}).get('user_id'))
        if not user.exists():
            return redirect('user:user_login')
        form = ChangePasswordForm(request.POST, instance=user.first())
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully')
            return redirect('user:user_login')
        messages.error(request, 'Invalid data found', extra_tags='danger')
        return redirect('user:user_change_password')
class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in')
            return redirect('user:index')
        return render(request, 'user/login.html', context={'title': 'Login'})

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Invalid Data found')
            return redirect('user:user_login')
        user = form.save()
        print(user)
        if isinstance(user, tuple):
            request.session['context'] = {
                'user_id': user[0].id,
            }
            return redirect('user:change_password')
        if user.is_authenticated:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('user:index')
        messages.error(request, 'Invalid credentials', extra_tags='danger')
        return redirect('user:user_login')


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('user:user_login')
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('user:user_login')

@login_required(login_url='user:user_login')
def remove_profile_pic(request):
    user = request.user
    user.profile_pic = None
    user.save()
    return JsonResponse(data={'message': 'Profile pic removed', 'tag': 'success'}, status=200,)

@has_permission(choices.ModuleChoices.USER.value,choices.PermissionChoices.VIEW.value)
def list_user_index(request):
        user = CustomUser.objects.all().values('id', 'username', 'first_name', 'last_name', 'email').order_by('id')
        groups = CustomGroup.objects.all().values('id', 'name').order_by('id')
        context = {
            'title': f'Users | {request.user.username}',
            'user_list': user,
            'group_list': groups
        }
        return render(request, 'user/user-manage.html', context=context)

class UserManageView(LoginRequiredMixin, View):
    login_url = 'user:user_login'
    

    @has_permission_class(choices.ModuleChoices.USER.value, choices.PermissionChoices.ADD.value)
    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            user = CustomUser.objects.get(pk=kwargs['pk'])
            group =list( user.customgroup_set.all().values_list('name', flat=True))
            # group = [g['name'] for g in group]
            return JsonResponse(data={'group': group}, status=200)
            
        form = UserAddFrom()
        context = {
        'title': f'Users | {request.user.username}',
        'form': form,
        }
        return render(request, 'user/add-edit-user.html', context=context)

    @has_permission_class(choices.ModuleChoices.USER.value, choices.PermissionChoices.ADD.value)
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            if kwargs.get('pk'):
                user = CustomUser.objects.get(pk=kwargs['pk'])
                data = request.POST.dict()
                data.pop('csrfmiddlewaretoken')
                print(data, list(user.customgroup_set.all().values_list('name', flat=True)))
                group_names = list(user.customgroup_set.all().values_list('name', flat=True))
                for data_key, data_value in data.items():
                    if data_key not in group_names:
                        print(data_key, data_value,group_names)
                        group = CustomGroup.objects.get(name=data_key)
                        user.customgroup_set.add(group)
                        user.save()
                for group_name in group_names:
                    if group_name not in data.keys():
                        group = CustomGroup.objects.get(name=group_name)
                        user.customgroup_set.remove(group)
                        user.save()
                return redirect('user:list_user')              
            else:
                form = UserAddFrom(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                else:
                    print(form.errors)
                    messages.error(request, 'Invalid data found', extra_tags='danger')

                return redirect('user:list_user')
