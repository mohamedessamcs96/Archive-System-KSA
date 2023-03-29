from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.conf import settings
# Create your models here.

GENDER_CHOICES=(
        ('M','Male'),
        ('F','Female')
    )

class UserAdmin(AbstractUser):
    fname=models.CharField(max_length=18,default='')
    lname=models.CharField(max_length=18,default='')
    email=models.EmailField(unique=True,null=False)
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES)
    birthdate=models.DateField(null=True)
    is_staff=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    password1=models.CharField(max_length=20)
    password2=models.CharField(max_length=20)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    #objects = CustomUserManager()
    def __str__(self):
        return self.fname + ' '+self.lname
    

class AddUser(models.Model):
    admin=models.ForeignKey(UserAdmin,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200)
    job  = models.CharField(max_length=200)
    jobnumber  = models.CharField(unique=True,primary_key=True,max_length=10)
    birthdate=models.DateField(null=True)
    image = models.ImageField(upload_to='images')
    notes=models.CharField(max_length=150)
    created=models.DateTimeField(auto_now_add=True)
    contract = models.ImageField(upload_to='images')
    def __str__(self):
        return self.jobnumber


class Document(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    created=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(AddUser,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.title

