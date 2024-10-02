import json
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.generic import View
from .permissions import has_permission, has_permission_class
from .models import CustomGroup, Module
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from . import choices

# Create your views here.


@login_required(login_url='user:user_login')
@has_permission(choices.ModuleChoices.GROUP.value, choices.PermissionChoices.VIEW.value)
def index(request):
    groups = CustomGroup.objects.all().values('name', 'id')
    context = {
        'groups': groups,
        'title': f'Group | {request.user.username}',
        'url_pattern': 'group:index',
        'link_name': 'Group',
        'button_name': 'Add Group',
    }
    return render(request, 'group/group.html', context=context)


@login_required(login_url='user:user_login')
@has_permission(choices.ModuleChoices.PERMISSION.value, choices.PermissionChoices.VIEW.value)
def permission(request, pk):
    print(pk, "pk")
    module = Module.objects.to_dict(pk)
    print(module)
    group = CustomGroup.objects.all().values('name', 'id')
    context = {
        'title': f'Permission | {request.user.username}',
        'url_pattern': 'group:permission',
        'link_name': 'Permission',
        'button_name': 'Add Permission',
        'modules': module,
        'groups': group,
        'selected': pk
    }
    return render(request, 'group/permissions.html', context=context)


class AddGroupView(LoginRequiredMixin, View):
    login_url = 'user:user_login'
    redirect_url = 'user:user_login'

    def get_object(self, pk):
        try:
            return CustomGroup.objects.get(pk=pk)
        except CustomGroup.DoesNotExist:
            return None

    @has_permission_class(choices.ModuleChoices.GROUP.value, choices.PermissionChoices.ADD.value)
    def post(self, request, *args, **kwargs):
        name = json.loads(request.body).get('group_name')
        if len(name) <= 0:
            return JsonResponse(data={'message': 'Empty Group Name', 'tag': 'danger'}, status=400,)
        if CustomGroup.objects.filter(name=name).exists():
            return JsonResponse(data={'message': 'Group already exists', 'tag': 'danger'}, status=400,)
        group = CustomGroup.objects.create(name=name)
        module_names = ['User', 'Group', 'Permission', 'Employees']
        modules = []
        for module_name in module_names:
            module = Module.objects.create(name=module_name)
            module.save()
            modules.append(module)

        group.module.set(modules)
        group.save()
        data = {
            'id': group.id,
            'name': group.name,
            'message': f'Group {group.name} added',
            'tag': 'success'
        }
        return JsonResponse(data=data, status=200,)


class UpdateGroupView(LoginRequiredMixin, View):
    login_url = 'user:user_login'

    def get_object(self, pk):
        try:
            return CustomGroup.objects.get(pk=pk)
        except CustomGroup.DoesNotExist:
            return None

    @has_permission_class(choices.ModuleChoices.GROUP.value, choices.PermissionChoices.UPDATE.value)
    def post(self, request, pk):
        try:
            instance = self.get_object(pk)
            if instance is None:
                messages.error(request, 'Group not found', extra_tags='danger')
                return redirect('group:index')
            name = request.POST.get('group_name')
            instance.name = name
            instance.save()
            messages.success(request, 'Group updated')
            return redirect('group:index')
        except IntegrityError:
            messages.error(request, 'Group already exists',
                           extra_tags='danger')
            return redirect('group:index')


class AddPermissionView(LoginRequiredMixin, View):
    def get_object(self, pk):
        try:
            return Module.objects.get(pk=pk)
        except Module.DoesNotExist:
            return None

    @has_permission_class(choices.ModuleChoices.PERMISSION.value, choices.PermissionChoices.UPDATE.value)
    def post(self, request, pk):
        instance = self.get_object(pk)
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        data_key = ['add', 'view', 'update', 'delete']
        for key in data_key:
            instance.permission[key] = True if data.get(key) == 'on' else False
            instance.save()
        return redirect(request.META.get('HTTP_REFERER'))
