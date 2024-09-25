from django.db import models
from django.db.models.manager import BaseManager
from user.models import CustomUser
## can you import BaseManager
# Create your models here.

class CustomModuleManager(BaseManager.from_queryset(models.QuerySet)):
  def to_dict(self, pk):
    return [module.to_dict() for module in self.filter(customgroup__id=pk)]
  
class Module(models.Model):
  name = models.CharField(max_length=100,null=False)
  permission = models.JSONField(default=dict({'add': False, 'view': True, 'update': False, 'delete': False}))
  objects = CustomModuleManager()
  def __str__(self):
    return f'{self.name}-{self.permission}'
  
  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'permissions': self.permission
    }


class CustomGroupManager(BaseManager.from_queryset(models.QuerySet)):
  def to_dict(self):
    return [group.to_dict() for group in self.all()]

class CustomGroup(models.Model):
  name = models.CharField(max_length=100, unique=True)
  module = models.ManyToManyField(Module)
  user = models.ManyToManyField(CustomUser)
  objects = CustomGroupManager()
  
  def __str__(self):
    return f'{self.name}'
  
  def to_dict(self):
    
    return {
      'id': self.id,
      'name': self.name,
      'module': [module.to_dict() for module in self.module.all()]
    }
  