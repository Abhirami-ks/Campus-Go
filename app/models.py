from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Destination(models.Model):
    path = models.CharField(max_length=100,null=True)
    
    
    
class Route(models.Model):
    path = models.ForeignKey(Destination, on_delete=models.DO_NOTHING, null=True)
    start= models.CharField(max_length=100,null=True)
    end=models.CharField(max_length=100,null=True)
    fees = models.IntegerField(null=True)
    
    
class CustomUser(AbstractUser):
    USER = (
        (1, 'ADMIN'),
        (2, 'FACULTY'),
        (3, 'STUDENT'),
        (4, 'DRIVER'),
    )
    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')
    status=models.CharField(max_length=80,null=True)
    destination = models.ForeignKey(Destination, on_delete=models.DO_NOTHING, null=True)
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING, null=True)
    license = models.CharField(max_length=100, null = True)
    phone = models.IntegerField(null=True)
    address = models.TextField(null=True)
    dept = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Bus(models.Model):
    number = models.IntegerField()
    users = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True)
    inch = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='incharge', null=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE,null=True)
    reg_no = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number


class Payment(models.Model):
    payee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING, null=True)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    feed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    Reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Location(models.Model):
    driver = models.CharField(max_length=19,null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)

    def __str__(self):
        return self.driver


