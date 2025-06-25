from django.db import models

# Create your models here.
class iProcess(models.Model):
    jobNumber = models.CharField(primary_key=True,max_length=100,default="")
    pid = models.CharField(max_length=100,default="",null=True)
    osUserName = models.CharField(max_length=100,default="",null=True)
    currentDevice = models.CharField(max_length=100,default="",null=True)
    routine  = models.CharField(max_length=100, default="",null=True)
    state = models.CharField(max_length=100,default="",null=True)
    userName = models.CharField(max_length=100,default="",null=True)

    def __str__(self):
        return self.name

