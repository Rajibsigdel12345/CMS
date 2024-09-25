from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.generic import View
from .permissions import has_permission, has_permission_class
from .models import CustomGroup,Module
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@login_required(login_url='user:user_login')
@has_permission('Group','view')
def index(request):
    groups = CustomGroup.objects.all().values('name','id')
    # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #     groups = CustomGroup.objects.to_dict()
    #     print("i am here")
    #     return JsonResponse(data={'groups': groups})
    context = {
        'groups': groups,
        'title': f'Group | {request.user.username}',
        'url_pattern': 'group:index',
        'link_name': 'Group',
        'button_name': 'Add Group',
    }
    return render(request, 'group/group.html', context = context)

@login_required(login_url='user:user_login') 
@has_permission('Permission','view')   
def permission(request, pk):
    print(pk, "pk")
    module = Module.objects.to_dict(pk)
    print(module)
    group = CustomGroup.objects.all().values('name','id')
    context = {
        'title': f'Permission | {request.user.username}',
        'url_pattern': 'group:permission',
        'link_name': 'Permission',
        'button_name': 'Add Permission',
        'modules': module,
        'groups': group,
        'selected': pk
    }
    return render(request, 'group/permissions.html', context = context)

class AddGroupView(LoginRequiredMixin,View):
    login_url = 'user:user_login'
    redirect_url = 'user:user_login'
    def get_object (self, pk):
        try:
            return CustomGroup.objects.get(pk = pk)
        except CustomGroup.DoesNotExist:
            return None
    @has_permission_class('Group','add')       
    def post(self, request,*args, **kwargs):        
        name = request.POST.get('group_name')
        if len(name)<=0:
            messages.error(request, 'Group name is required',extra_tags='danger')
            return redirect('group:index')
        if CustomGroup.objects.filter(name = name).exists():
            messages.error(request, 'Group already exists',extra_tags='danger')
            return redirect('group:index')
        group = CustomGroup.objects.create(name = name)
        module_names = ['User','Group','Permission','Employees']
        modules = []
        for module_name in module_names:
            module = Module.objects.create(name = module_name)
            module.save()
            modules.append(module)
        
        group.module.set(modules)
        group.save()
        messages.success(request, 'Group added')
        return redirect('group:index')

class UpdateGroupView(LoginRequiredMixin,View):
    login_url = 'user:user_login'
    
    def get_object(self, pk):
        try:
            return CustomGroup.objects.get(pk = pk)
        except CustomGroup.DoesNotExist:
            return None
    
    @has_permission_class('Group','update')
    def post(self, request,pk):
       try: 
            instance  = self.get_object(pk)
            if instance is None:
                messages.error(request, 'Group not found',extra_tags='danger')
                return redirect('group:index')
            name = request.POST.get('group_name')
            instance.name = name
            instance.save()
            messages.success(request, 'Group updated')
            return redirect('group:index')
       except IntegrityError:
            messages.error(request, 'Group already exists',extra_tags='danger')
            return redirect('group:index')        

class AddPermissionView(LoginRequiredMixin,View):
    def get_object(self, pk):
        try:
            return Module.objects.get(pk = pk)
        except Module.DoesNotExist:
            return None
    
    @has_permission_class('Permission','update')
    def post (self, request,pk):
        instance = self.get_object(pk)
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        data_key = ['add','view','update','delete']
        for key in data_key:
            instance.permission[key] = True if data.get(key) == 'on' else False
            instance.save()
        return redirect(request.META.get('HTTP_REFERER'))