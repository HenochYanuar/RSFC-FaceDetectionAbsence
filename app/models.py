from django.db import models

# Create your models here.
class Users(models.Model):
    nik = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    divisi = models.CharField(max_length=50,null=True)
    photo = models.ImageField(upload_to='static/img')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Admins(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    is_superadmin = models.BooleanField(default=False)
    nik = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class InAbsences(models.Model):
    id = models.AutoField(primary_key=True)
    nik = models.ForeignKey(Users, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OutAbsences(models.Model):
    id = models.AutoField(primary_key=True)
    nik = models.ForeignKey(Users, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
