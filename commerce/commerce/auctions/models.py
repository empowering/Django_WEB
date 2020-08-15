from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime    
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Models: Your application should have 
# at least three models in addition to the User model:
# one for auction listings, one for bids, and one for comments made on auction listings. 
# It’s up to you to decide what fields each model should have, and what the types of those fields should be. 
# You may have additional models if you would like.

class Listing(models.Model):

    OPTIONS = (
    ('clothing','Clothing'),
    ('crafts','Crafts'),
    ('home','Home'), 
    ('pet','Pet'), 
    )

    list_id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=OPTIONS)
    likes = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = ProcessedImageField(
               upload_to='auctions', # ?? ??
               processors=[ResizeToFill(600,600)], # ??? ?? ??
               format='JPEG', # ?? ??(???)
               options= {'quality': 90 }, # ?? ?? ?? ?? (JPEG ??? ??)
        )

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

class Bidding(models.Model):
    bidder = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bidder')
    item = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='item')
    bids = models.IntegerField()

    def __str__(self):
        return f"{self.bids} to {self.item.name} by {self.bidder}"
