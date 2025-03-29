from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment


def index(request):
    if request.user.is_authenticated:
        listings = Listing.objects.all()
    else:
        listings = Listing.objects.none()

    return render(request, "auctions/index.html", {
        "listings": listings
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

def listing_form(request):
    return render(request, "auctions/listing_form.html")

def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]

        listing = Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image=image_url,
            product_category=category,
            creator=request.user
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/create_listing.html")

def listing_detail(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids = listing.bids.all()
    comments = listing.comments.all()

    highest_bid = listing.bids.order_by('-amount').first()
    highest_bid_amount = highest_bid.amount if highest_bid else listing.starting_bid

    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "highest_bid_amount": highest_bid_amount
    })

def bid(request, listing_id):
    if request.method == "POST":
        amount = float(request.POST["bid_amount"])
        listing = Listing.objects.get(pk=listing_id)
        
        highest_bid = listing.bids.order_by('-amount').first()
        highest_bid_amount = highest_bid.amount if highest_bid else listing.starting_bid

        if amount > highest_bid_amount:
            bid = Bid(
                listing=listing,
                bid_user=request.user,
                amount=amount
            )
            bid.save()
            return HttpResponseRedirect(reverse("listing_detail", args=(listing_id,)))
        else:
            # Display an error message if the bid is not higher
            return render(request, "auctions/listing_detail.html", {
                "listing": listing,
                "bids": listing.bids.all(),
                "comments": listing.comments.all(),
                "error_message": f"Your bid must be higher than ${highest_bid_amount:.2f}."
            })

def comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        listing = Listing.objects.get(pk=listing_id)
        comment = Comment(
            listing=listing,
            comment_user=request.user,
            comment=comment
        )
        comment.save()
        return HttpResponseRedirect(reverse("listing_detail", args=(listing_id,)))

def add_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.user in listing.watchlist_users.all():
        listing.watchlist_users.remove(request.user)
    else:
        listing.watchlist_users.add(request.user)
    return HttpResponseRedirect(reverse("listing_detail", args=(listing_id,)))

def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    # Ensure only the creator can close the auction
    if request.user == listing.creator:
        # Get the highest bid
        highest_bid = listing.bids.order_by('-amount').first()

        # If there is a highest bid, set the winner
        if highest_bid:
            listing.winner_user = highest_bid.bid_user

        # Mark the listing as inactive
        listing.is_active = False
        listing.save()

    return HttpResponseRedirect(reverse("listing_detail", args=(listing_id,)))

def watchlist(request):
    if request.user.is_authenticated:
        # Get all listings in the user's watchlist
        watchlist_items = request.user.watchlist.all()
    else:
        watchlist_items = []

    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

def categories(request):
    # Get a list of all unique categories
    categories = Listing.objects.values_list('product_category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, category_name):
    # Get all active listings in the specified category
    listings = Listing.objects.filter(product_category=category_name, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category_name": category_name,
        "listings": listings
    })

def sold_listings (request):
    sold_listings = Listing.objects.filter(winner_user__isnull=False)
    
    for listing in sold_listings:
        highest_bid = listing.bids.order_by('-amount').first()
        listing.highest_bid_amount = highest_bid.amount if highest_bid else None

    return render(request, "auctions/sold_listings.html", {
        "sold_listings": sold_listings
    })