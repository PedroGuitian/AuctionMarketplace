from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    image = models.URLField(blank=True) # Stores the URL of the image
    product_category = models.CharField(max_length=64, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    winner_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_listings", blank=True, null=True)
    watchlist_users = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"The {self.title} listing, created by {self.creator} at {self.posted_at} is active:{self.is_active}."

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bid_user} bid {self.amount} on {self.listing} at {self.bid_time}."

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment_user} commented on {self.listing} at {self.comment_time}."