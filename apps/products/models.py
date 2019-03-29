from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

# Create your models here.
class Product(models.Model):
    category = models.OneToOneField(Category)

    name = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    img = models.CharField(max_length=100)
    new_price = models.IntegerField(default=0)
    old_price = models.IntegerField(default=0)
    color = models.CharField(max_length=100) 
    size = models.CharField(max_length=100)
    numberBuy = models.IntegerField(default=0)
    more = models.TextField(max_length=1000)

    #time create and update of a post
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

# class DetailProduct(models.Model):
