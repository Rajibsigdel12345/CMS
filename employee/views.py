from django.shortcuts import render
from django.views import View

from .models import Employee
from .forms import EmployeeForm
from django.shortcuts import redirect
from django.db import transaction

# Create your views here.
def index(request):
  employees = Employee.objects.all().values('first_name','last_name','email','phone','address')
  print(employees)
  context = {
      'title': f'Employee | {request.user.username}',
      'url_pattern': 'employee:index',
      'employees': employees
  }
  return render(request, 'employee/employee.html', context = context)

def employee_list(request):
  context = {
      'title': f'Employee | {request.user.username}',
      'url_pattern': 'employee:index',
  }
  return render(request, 'employee/employee-list.html', context = context)


class EmployeeAddView(View):
  def get(self, request):
    form = EmployeeForm()
    context = {
      'title': f'Employee | {request.user.username}',
      'url_pattern': 'employee:addemployee',
      'form': form
    }
    return render(request, 'employee/employee-add.html', context = context)
  
  def post(self, request):
   with transaction.atomic(): 
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