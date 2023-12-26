from django.db import models
from django.contrib.auth.models import User
from service.models import Task
# from django_countries.fields import CountryField


# Create your models here.


class Department(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    Image = models.ImageField(upload_to="img/", default="img/logo.png")
    supervisor = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_department')
    worker = models.ManyToManyField(User, related_name='working_departments')
    task = models.ForeignKey(Task, related_name='assigned_tasks', on_delete=models.CASCADE)

    def __str__(self) -> str:
       return f"{self.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    # nationality = CountryField()
    avatar = models.ImageField(upload_to="img/", default="img/avatar.png")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    
    def __str__(self):
      return f" - {self.user.first_name}" 

   
