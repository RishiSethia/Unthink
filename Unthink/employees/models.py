from django.db import models

# Create your models here.
class Employee(models.Model):
    empcode = models.CharField(max_length=10)
    dept = models.CharField(max_length=70)
    score = models.IntegerField()
    createdate = models.DateTimeField()
    lastModified = models.DateTimeField(auto_now_add=True, blank=True)
