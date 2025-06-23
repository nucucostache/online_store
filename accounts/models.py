from django.db import models
from django.utils import timezone


class Role(models.Model):
    role = models.CharField(max_length=50)
    
    def __str__(self):
        return self.role

class Account(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="images/", null=True, blank=True)   
    mail = models.CharField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.username




    

