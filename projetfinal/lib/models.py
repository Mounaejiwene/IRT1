from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class LibraryManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class Library(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name_lib = models.CharField(max_length=60, null=False)
    username = models.CharField(max_length=10, unique=True, null=False)
    email = models.EmailField(max_length=60, unique=True, null=False)
    password = models.CharField(max_length=80, null=False)
    phone_number = models.CharField(max_length=15, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = LibraryManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'Library'

    def __str__(self):
        return self.email

class Livre(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Human Development', 'Human development'),
        ('Romance', 'Romance'),
        ('Fiction', 'Fiction'),
    ]

    Id_livre = models.AutoField(primary_key=True)
    Name_book = models.CharField(max_length=50, default=None)
    Authour_name = models.CharField(max_length=20, null=True, blank=True)
    Genre = models.CharField(max_length=20, choices=GENRE_CHOICES, null=True, blank=True)
    Image = models.ImageField(upload_to='images/',null=True,blank=True)
    Stock = models.IntegerField(default=1)
    Id_lib = models.ForeignKey(Library, on_delete=models.CASCADE)
    Prix = models.FloatField(default=100)
    Description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Livre'

    def __str__(self):
        return self.Name_book
