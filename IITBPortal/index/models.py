from django.db import models
from django.contrib.auth.models import Permission, User
# Create your models here.

class student(models.Model):
    user = models.ForeignKey(User, default=1)
    fname = models.CharField(max_length=100,default='')
    lname = models.CharField(max_length=100,default='')
    email_id = models.CharField(max_length=150,default='')
    login_id = models.CharField(max_length=100,default='')

    first_name = models.CharField(max_length=250,default="")
    last_name = models.CharField(max_length=250,default="")
    phone = models.CharField(max_length=250,default="")
    university = models.CharField(max_length=250,default="")
    graduation = models.CharField(max_length=250,default="")
    year = models.CharField(max_length=250,default="")
    city = models.CharField(max_length=250,default="")
    
    def __str__(self):
        return self.login_id + " - " + self.university

class courses(models.Model):
    std = models.ForeignKey(student, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=20,default="")
    course_name = models.CharField(max_length=250,default="")

    def __str__(self):
        return self.course_code

