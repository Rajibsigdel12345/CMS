from django.db.models import TextChoices

class PermissionChoices(TextChoices):
  ADD = 'add', 'add'
  VIEW = 'view', 'view'
  UPDATE = 'update', 'update'
  DELETE = 'delete', 'delete'

class ModuleChoices(TextChoices):
  USER = 'User', 'User'
  GROUP = 'Group', 'Group'
  PERMISSION = 'Permission', 'Permission'
  EMPLOYEES = 'Employees', 'Employees'
  
  