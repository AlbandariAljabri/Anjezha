from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Department(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    worker = models.ManyToManyField(User, related_name='working_departments')
    image = models.ImageField(upload_to="img/", default="img/logo.png")
    supervisor = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='supervised_department')

    def __str__(self) -> str:
       return f"{self.title}"