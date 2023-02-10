from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    name=models.CharField(max_length=150)
    description=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
