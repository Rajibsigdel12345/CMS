from django.shortcuts import render
from django.views import View

from group.permissions import has_permission, has_permission_class
from group import choices

from .models import Employee
from .forms import EmployeeForm
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@login_required(login_url='user:user_login')
@has_permission(choices.ModuleChoices.EMPLOYEES.value,choices.PermissionChoices.VIEW.value)
def index(request):
  employees = Employee.objects.all().values('first_name','last_name','email','phone','address')
  print(employees)
  context = {
      'title': f'Employee | {request.user.username}',
      'url_pattern': 'employee:index',
      'employees': employees
  }
  return render(request, 'employee/employee.html', context = context)



class EmployeeAddView(LoginRequiredMixin,View):
  login_url = 'user:user_login'
 
  @has_permission_class(choices.ModuleChoices.EMPLOYEES.value,choices.PermissionChoices.ADD.value)
  def get(self, request):
    form = EmployeeForm()
    context = {
      'title': f'Employee | {request.user.username}',
      'url_pattern': 'employee:addemployee',
      'form': form
    }
    return render(request, 'employee/employee-add.html', context = context)
  
  @has_permission_class(choices.ModuleChoices.EMPLOYEES.value,choices.PermissionChoices.ADD.value)
  def post(self, request, *args, **kwargs):
    with transaction.atomic():
      if kwargs.get('pk'):
        employee = Employee.objects.get(pk=kwargs.get('pk'))
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
      else:
        form = EmployeeForm(request.POST, request.FILES)
      if form.is_valid():
        instance =form.save()
        print(instance)
        return redirect('employee:index')
      else:
        context = {
          'title': f'Employee | {request.user.username}',
          'url_pattern': 'employee:addemployee',
          'form': form
        }
        return render(request, 'employee/employee-add.html', context = context)