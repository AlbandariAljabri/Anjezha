from django.db import models
from django.contrib.auth.models import User 
from service.models import *
from department.models import *
# from django_countries.fields import CountryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    # nationality = CountryField()
    avatar = models.ImageField(upload_to="img/", default="img/avatar.png")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, default=None)
    
    
    def __str__(self):
      return f" - {self.user.first_name}" 

   

