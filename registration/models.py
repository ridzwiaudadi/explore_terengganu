from django.db import models

# Create your models here.


class User(models.Model):
    userID= models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    userphonenum = models.CharField(max_length=15)
    useremail = models.EmailField()

class Event (models.Model):
    eventID= models.AutoField(primary_key=True)
    eventname=models.CharField(max_length=100)
    eventlocation=models.CharField(max_length=100)
    eventprice= models.FloatField()
    startdate=models.DateField()
    enddate= models.DateField()

class Register (models.Model):
    registerID=models.AutoField(primary_key=True)
    userID=models.ForeignKey(User, on_delete=models.CASCADE)
    eventID=models.ForeignKey(Event, on_delete=models.CASCADE)
    numofticket=models.IntegerField()
    registerdate= models.DateField()
    paymentmethod= models.CharField(max_length= 20)
    totalprice= models.IntegerField()
    registerstatus=models.CharField(max_length=15)

class Review (models.Model):
    reviewID= models.AutoField(primary_key=True)
    userID=models.ForeignKey(User, on_delete=models.CASCADE)
    reviewcomment=models.TextField()
