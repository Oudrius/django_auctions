from django.forms import ModelForm
from auctions.models import Listing, Bid, Comment


# Create a form from Listing model to use in 'create_listing' template
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "starting_bid", "description", "category", "image", "image_url"]

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        labels = {
            "content": ''
        }
        fields = ["content"]