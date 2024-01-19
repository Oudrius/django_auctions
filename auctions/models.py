from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlist_items")


class Listing(models.Model):
    title = models.CharField(max_length=120)
    starting_bid = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.CharField(max_length=360)
    # default=4 sets default to 'Uncategorized'
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=4, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_creator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)
    image_url = models.CharField(max_length=1024, blank=True)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name="listing_winner")

    def __str__(self):
        return f"Item id: {self.id}: Title: {self.title}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=4, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    
    def __str__(self):
        return f"Bid id {self.id} Bid: {self.amount} on {self.listing.title}"
    

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT)
    commentator = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    content = models.CharField(max_length=250)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment id {self.id}: Comment on {self.listing.title}: {self.content}"


class Category(models.Model):
    title = models.CharField(max_length=60)

    def __str__(self):
        return f"Category id: {self.id}: Category: {self.title}"