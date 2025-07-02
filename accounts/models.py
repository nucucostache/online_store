from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Role(models.Model):
    role = models.CharField(max_length=50)
    
    
    
    
    def __str__(self):
        return self.role

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="images/", null=True, blank=True)   
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user.username if self.user else "No User"





    

