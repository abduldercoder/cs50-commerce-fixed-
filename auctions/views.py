from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ListingForm
from django.shortcuts import get_object_or_404
from .models import User
from .models import Listing,Bid, Comment
from django import forms
from django.contrib import messages



def index(request):
    listings = Listing.objects.filter(active=True)
    category_choices = Listing.CATEGORY_CHOICES  # add this line
    return render(request, "auctions/index.html", {
        "listings": listings,
        "category_choices": category_choices  # pass to template
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
def create_listing(request):
    """
    Display the blank form (GET) and save a new auction listing (POST).
    After successful creation, redirect to the index page (or your desired page).
    """
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user  # assumes Listing has an 'owner' FK to User
            listing.save()
            return redirect("index")  # adjust name if your index URL is named differently
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {"form": form})

from .models import Bid  # Make sure this is imported

def listing_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    # Get current highest bid (or None if no bids yet)
    highest_bid = listing.bids.order_by("-amount").first()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "highest_bid": highest_bid,
    })


@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.user in listing.watchers.all():
        listing.watchers.remove(request.user)
    else:
        listing.watchers.add(request.user)

    return redirect("listing_view", listing_id=listing.id)




@login_required
def watchlist_view(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })





@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    # ❗ Prevent bidding on closed listings
    if not listing.active:
        messages.error(request, "This auction is closed. You cannot place a bid.")
        return redirect("listing_view", listing_id=listing.id)

    try:
        bid_amount = float(request.POST["bid_amount"])
    except (KeyError, ValueError):
        messages.error(request, "Invalid bid.")
        return redirect("listing_view", listing_id=listing.id)

    # Check if bid is valid
    current_max_bid = listing.bids.order_by("-amount").first()
    min_bid = listing.starting_bid if not current_max_bid else current_max_bid.amount

    if bid_amount <= min_bid:
        messages.error(request, f"Bid must be greater than ${min_bid:.2f}.")
    else:
        Bid.objects.create(
            listing=listing,
            bidder=request.user,
            amount=bid_amount
        )
        messages.success(request, "Your bid was placed successfully!")

    return redirect("listing_view", listing_id=listing.id)






@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.user != listing.creator:
        messages.error(request, "You are not authorized to close this auction.")
        return redirect("listing_view", listing_id=listing.id)

    listing.active = False
    listing.save()

    messages.success(request, "The auction has been closed.")
    return redirect("listing_view", listing_id=listing.id)



@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    content = request.POST.get("comment_content")

    if not content:
        messages.error(request, "Comment cannot be empty.")
    else:
        Comment.objects.create(listing=listing, user=request.user, content=content)
        messages.success(request, "Comment added.")

    return redirect("listing_view", listing_id=listing.id)

@login_required
def my_listings(request):
    listings = Listing.objects.filter(creator=request.user)
    return render(request, "auctions/my_listings.html", {
        "listings": listings
    })

def category_listings(request, category_name):
    listings = Listing.objects.filter(category=category_name, active=True)
    return render(request, "auctions/category.html", {
        "category": category_name,
        "listings": listings
    })



@login_required
def reopen_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.user != listing.creator:
        messages.error(request, "You are not authorized to reopen this auction.")
        return redirect("listing_view", listing_id=listing.id)

    if listing.active:
        messages.info(request, "This auction is already open.")
    else:
        listing.active = True
        listing.save()
        messages.success(request, "The auction has been reopened.")

    return redirect("listing_view", listing_id=listing.id)
