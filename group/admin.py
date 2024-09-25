from django.contrib import admin
# import ModelAdmin

from . import models
# Register your models here.

@admin.register(models.CustomGroup)
class CustomGroupAdmin(admin.ModelAdmin):
  list_display = ['name']
  search_fields = ['name']
  list_filter = ['name']
  ordering = ['name']  


# @admin.register(models.Permission)
# class PermissionAdmin(admin.ModelAdmin):
#   list_display = ['name']
#   search_fields = ['name']
#   list_filter = ['name']
#   ordering = ['name']

@admin.register(models.Module)
class ModuleAdmin(admin.ModelAdmin):
  list_display = ['name']
  search_fields = ['name']
  list_filter = ['name']
  ordering = ['name']