from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class Library(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name_lib = models.CharField(max_length=60,null=False)
    username=models.CharField(max_length=10,unique=True,null=False)
    email = models.CharField(max_length=60,unique=True,null=False)
    password = models.CharField(max_length=80,null=False)
    
    class Meta:
        db_table = 'Library'

    

 

class Livre(models.Model):
    Id_livre = models.AutoField(primary_key=True)
    Name_book = models.CharField(max_length=50, default=None)
    Authour_name = models.CharField(max_length=20, null=True, blank=True)
    Genre = models.CharField(max_length=20, null=True, blank=True)
    Image = models.ImageField(upload_to='images/')
    Stock = models.IntegerField()  
    Id_lib = models.ForeignKey(Library, on_delete=models.CASCADE)
    Prix = models.FloatField(default=100)

    class Meta:
        db_table = 'Livre'
        

  