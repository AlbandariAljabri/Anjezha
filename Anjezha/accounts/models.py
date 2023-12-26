from django.db import models
from django.contrib.auth.models import User
# from django_countries.fields import CountryField


# Create your models here.


class Department(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    Image = models.ImageField(upload_to="img/" , default="img/logo.png")

    def __str__(self) -> str:
       return f"{self.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    # nationality = CountryField()   
    avatar = models.ImageField(upload_to="img/" , default="img/avatar.png")
    department = models.ForeignKey(Department , on_delete=models.CASCADE )
    
    def __str__(self):
      return f" - {self.user.first_name}" 

