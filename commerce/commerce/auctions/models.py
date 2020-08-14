from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime    
from django.conf import settings

# Models: Your application should have 
# at least three models in addition to the User model:
# one for auction listings, one for bids, and one for comments made on auction listings. 
# It’s up to you to decide what fields each model should have, and what the types of those fields should be. 
# You may have additional models if you would like.

class Listing(models.Model):
    list_id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    likes = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField()

    def __str__(self):
        return f"{self.list_id} : {self.name} / {self.price} / {self.date}"

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name='watchlist')
    
class Comment(models.Model):
    post = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.CharField(max_length = 50)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text