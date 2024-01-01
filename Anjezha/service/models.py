from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    address = models.URLField()
    workers = models.ManyToManyField(User , related_name='assigned_tasks')
    supervisor = models.ForeignKey(User, on_delete=models.PROTECT , related_name='supervised_tasks',null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    # completed = models.BooleanField(default=False)

    WORKER_STATUS_CHOICES = (('none', 'None'),('in_progress', 'In Progress'),)
    worker_status = models.CharField(max_length=20, choices=WORKER_STATUS_CHOICES, default='none')

    SUPERVISOR_STATUS_CHOICES = (('uncompleted', 'Uncompleted'),('completed', 'Completed'),)
    supervisor_status = models.CharField(max_length=20, choices=SUPERVISOR_STATUS_CHOICES, default='uncompleted')

    def get_selected_workers(self):
        return self.workers.all()
    def duration(self):
        return self.end_date - self.start_date
    def __str__(self):
        return f"{self.name} task created by  {self.supervisor}"


class Comment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    task = models.ForeignKey(Task , on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="img/" )
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.user} : {self.content}"
    
class Reply(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="img/" )
