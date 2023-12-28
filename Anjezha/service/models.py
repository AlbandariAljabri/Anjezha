from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    address = models.URLField()
    workers = models.ManyToManyField(User , related_name='assigned_tasks',null=True)
    supervisor = models.ForeignKey(User, on_delete=models.PROTECT , related_name='supervised_tasks',null=True)

    def get_selected_workers(self):
        return self.workers.all()
    def duration(self):
        return self.end_date - self.start_date


class Comment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    task = models.ForeignKey(Task , on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="img/" , default="img/logo.png")
