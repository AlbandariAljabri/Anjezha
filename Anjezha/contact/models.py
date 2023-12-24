from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Contact(models.Model):
    status_choices = models.TextChoices("status_choices", ["Unread", "Read", "Replied"])
    user = models.ForeignKey(User ,  on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=status_choices.choices, default='Unread')
    file = models.FileField()

    def __str__(self):
        return self.subject
