from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal

from .forms import ListingForm, BidForm, CommentForm
from .models import User, Listing, Bid, Comment, Category


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        # Add current user to 'created_by' field
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.created_by = request.user
            new_listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            print("Form errors: ", form.errors)
            return render(request, "auctions/create.html", {
                "form": form
            })
    else:
        return render(request, "auctions/create.html", {
            "form": ListingForm()
        })
    
def listing(request, listing_id):
    # Get current listing object
    listing = Listing.objects.get(id=listing_id)
    # Get current listing comments
    comments = Comment.objects.filter(listing=listing)
    if request.method == "POST":
        # Get current user object and action
        current_user = User.objects.get(username=request.user)
        action = request.POST.get('action')

        # Handle watchlist
        if action == 'watchlist':
            # Add/Remove listing to/from watchlist
            if listing in current_user.watchlist.all():
                current_user.watchlist.remove(listing)
            else:
                current_user.watchlist.add(listing)

        # Handle bidding
        if action == 'bid':
            # Get bid amount
            new_amount = request.POST.get('amount')
            # Create a new bid
            if Decimal(new_amount) > Decimal(listing.starting_bid):
                new_bid = Bid(listing=listing, amount=new_amount, bidder=current_user)
                new_bid.save()
                # Update current price
                listing.starting_bid = new_bid.amount
                listing.save()
            else:
                messages.error(request, "New bid is lesser than the current highest bid.")
            
        # Handle auction close:
        if action == 'close_auction':
            # Get the highest bidder
            highest_bid = Bid.objects.filter(listing=listing).latest('bid_time')
            # Update auction winner
            listing.winner = highest_bid.bidder
            # Change listing status and save listing
            listing.is_active = False
            listing.save()
        
        # Handle comment posting:
        if action == 'add_comment':
            # Get comment content
            comment_content = request.POST.get('content')
            # Add new comment
            new_comment = Comment(listing=listing, content=comment_content, commentator=current_user)
            new_comment.save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid": BidForm(),
            "comments": comments,
            "comment_form": CommentForm()
        })

@login_required
def watchlist(request):
    # Get watchlist entries for current user
    user = User.objects.get(username = request.user)
    watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def categories(request):
    # Get all categories
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, title):
    # Get category id (__iexact ignores query string case)
    category_id = Category.objects.get(title__iexact=title)
    # Get listings based on category id
    listings = Listing.objects.filter(category=category_id)
    return render(request, "auctions/category.html", {
        "title": title,
        "listings": listings
    })