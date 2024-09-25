from django.db import models

# Create your models here.
class Employee(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField(max_length=100)
  phone = models.CharField(max_length=100)
  address = models.TextField()
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  zip = models.CharField(max_length=100)
  country = models.CharField(max_length=100)
  date_of_birth = models.DateField()
  date_of_joining = models.DateField()
  department = models.CharField(max_length=100)
  designation = models.CharField(max_length=100)
  salary = models.DecimalField(max_digits=10, decimal_places=2)
  profile_pic = models.ImageField(upload_to='media', default='media/default.jpg')
  user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='employee', null=True)
  
  
  def __str__(self):
    return self.first_name + ' ' + self.last_name
  
  def to_dict(self):
    return {
      'id': self.id,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'email': self.email,
      'phone': self.phone,
      'address': self.address,
      'city': self.city,
      'state': self.state,
      'zip': self.zip,
      'country': self.country,
      'date_of_birth': self.date_of_birth,
      'date_of_joining': self.date_of_joining,
      'department': self.department,
      'designation': self.designation,
      'salary': self.salary,
      'profile_pic': self.profile_pic.url
    }
  class Meta:
    ordering = ['first_name']
    verbose_name = 'Employee'
    verbose_name_plural = 'Employees'