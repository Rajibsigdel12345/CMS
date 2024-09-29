from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  profile_pic = models.ImageField(upload_to='media', default='media/default.png')
  
  def __str__(self):
    return self.username
  
  def to_dict(self):
    return {
      'id': self.id,
      'username': self.username,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'email': self.email,
      'is_staff': self.is_staff,
      'is_active': self.is_active,
      'date_joined': self.date_joined,
    }

  def save(self, *args, **kwargs):
    if not self.profile_pic:
      self.profile_pic = 'media/default.png'
    return super().save(*args, **kwargs)
  