from django.urls import path
from .views import AddGroupView, index,permission,AddPermissionView, UpdateGroupView

app_name = 'group'
urlpatterns = [
  path('', index, name='index'),
  path('permission/<int:pk>/', permission, name='permission'),
  path('add/', AddGroupView.as_view(), name='addgroup'),
  path('add/<int:pk>/', UpdateGroupView.as_view(), name='update_group'),
  path('permission/add/<int:pk>/', AddPermissionView.as_view(), name='addpermission')
] 