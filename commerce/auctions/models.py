from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=144)
    startingBid = models.CharField(max_length=64)
    imgUrl = models.CharField(max_length=64)
    owner = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.owner} ({self.item}) {self.price}"


class Bid(models.Model):
    user = models.CharField(max_length=64)
    bid = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user} {self.bid}"


class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=144)

    def __str__(self):
        return f"{self.user} {self.comment}"
