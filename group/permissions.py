# Basepermissions
from django.contrib import messages
from .models import CustomGroup , Module
from django.shortcuts import redirect

def has_permission(module_para,permission_para):
  def decorator(view_func):
    def wrapper_func(request, *args, **kwargs):
      if request.user.is_superuser:
        return view_func(request, *args, **kwargs)
      group = CustomGroup.objects.filter(user__id=request.user.id)
      print(group)
      module = Module.objects.filter(permission__contains={permission_para:True},customgroup__in=group,name=module_para)
      print(module)
      if not module.exists() or not module.first().permission[permission_para]:
        messages.error(request, 'You do not have permission to perform this action', extra_tags='danger')
        return redirect(request.META.get('HTTP_REFERER')) if not module_para == 'User' and not permission_para=='view' else redirect('user:index')
      return view_func(request, *args, **kwargs)
    return wrapper_func
  return decorator

def has_permission_class(module_para,permission_para):
  def decorator(view_func):
    def wrapper_func(self,request, *args, **kwargs):
      if request.user.is_superuser:
        return view_func(self,request, *args, **kwargs)
      group = CustomGroup.objects.filter(user__id=request.user.id)
      print(group)
      modules = Module.objects.filter(permission__contains={permission_para:True},customgroup__in=group,name=module_para)
      print(modules)
      print(module_para,permission_para)
      for module in modules:
        if module.permission.get(permission_para):
          return view_func(self,request, *args, **kwargs)
      messages.error(request, 'You do not have permission to perform this action', extra_tags='danger')
      return redirect(request.META.get('HTTP_REFERER')) if not module_para == 'User' and not permission_para=='view' else redirect('user:index')
    return wrapper_func
  return decorator