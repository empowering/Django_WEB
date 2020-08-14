from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime    

# Models: Your application should have 
# at least three models in addition to the User model:
# one for auction listings, one for bids, and one for comments made on auction listings. 
# It’s up to you to decide what fields each model should have, and what the types of those fields should be. 
# You may have additional models if you would like.

class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    image = models.ImageField()

    def __str__(self):
        return f"List added"

