from django.urls import path
from .views import index , EmployeeAddView

app_name = 'employee' 
urlpatterns = [
              path('', index, name='index'),   
              path('add/', EmployeeAddView.as_view(), name='addemployee'),   
 ]