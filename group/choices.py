from django.db.models import TextChoices

class PermissionChoices(TextChoices):
  ADD = 'add', 'Add'
  VIEW = 'view', 'View'
  UPDATE = 'update', 'Update'
  DELETE = 'delete', 'Delete'

class ModuleChoices(TextChoices):
  USER = 'User', 'User'
  GROUP = 'Group', 'Group'
  PERMISSION = 'Permission', 'Permission'
  EMPLOYEES = 'Employees', 'Employees'
  
  