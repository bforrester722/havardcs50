from datetime import datetime
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import ListingForm
from .models import Bid, Comment, User, Listing, CATEGORY_CHOICES


# add highest bind to listings
def add_highest_bid_to_listings(listings):
    for listing in listings:
        bids = listing.bids.all().order_by("bid")
        if bids:
            listing.highest_bid = bids.last().bid
        else:
            listing.highest_bid = listing.startingBid
    return listings


# default view showing active listings
def index(request):
    listings = Listing.objects.filter(closed=False)
    listings = add_highest_bid_to_listings(listings)
    return render(request, "auctions/index.html", {"listings": listings})


#  view showing categories
def categories(request, category=None):
    listings = Listing.objects.filter(category=category)
    listings = add_highest_bid_to_listings(listings)
    return render(
        request,
        "auctions/categories.html",
        {
            "categories": CATEGORY_CHOICES,
            "category": listings,
        },
    )


#  view showing specfic listing
def listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    try:
        bids = listing.bids.all()
        comments = listing.comments.all()
        highest_bid = bids.last().bid if bids else listing.startingBid
        minimum_bid = highest_bid + Decimal("0.01")
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "bids": bids.count(),
            "highest_bid": highest_bid,
            "minimum_bid": minimum_bid,
            "comments": comments,
        },
    )


#  view showing users watchlist
@login_required
def watchlist(request):
    # user = User.objects.get(pk=int(request.user.id))
    listings = request.user.watching.all()
    listings = add_highest_bid_to_listings(listings)
    return render(
        request,
        "auctions/watchlist.html",
        {"listings": listings},
    )


#  view for user to create a listing
@login_required
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            # Set the owner field to the currently logged-in user
            form.instance.owner = request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {"form": ListingForm()})


# Form Actions
@login_required
def handle_action(request, listing_id, action_type):
    if request.method == "POST":
        listing = get_object_or_404(Listing, id=listing_id)
        user = request.user
        # adds bid to listing
        if action_type == "bid":
            try:
                action_data = request.POST["bid"]
                new_action = Bid(listing_id=listing, user=request.user, bid=action_data)
                new_action.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            except KeyError:
                return HttpResponseBadRequest("Bad Request: No bid provided")
        # closes the listing and determines the winner
        elif action_type == "close":
            if not listing.bids.exists():
                return HttpResponseBadRequest(
                    "Bad Request: No bids to close the listing"
                )

            listing.closed = True
            listing.winner = listing.bids.last().user
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        # adds comment to listing
        elif action_type == "comment":
            try:
                action_data = request.POST["comment"]
                new_action = Comment(
                    listing_id=listing,
                    user=request.user,
                    comment=action_data,
                    date_time=datetime.now(),
                )
                new_action.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            except KeyError:
                return HttpResponseBadRequest("Bad Request: No comment provided")
        # toggles the user's watchlist status for the listing
        elif action_type == "change_watchlist":
            if user.is_authenticated:
                if listing in user.watching.all():
                    user.watching.remove(listing)
                else:
                    user.watching.add(listing)

                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                return HttpResponseBadRequest("Bad Request: User not authenticated")

    return HttpResponseBadRequest("Bad Request: Invalid HTTP method")


def bid(request, listing_id):
    return handle_action(request, listing_id, "bid")


def change_watchlist(request, listing_id):
    return handle_action(request, listing_id, "change_watchlist")


def close(request, listing_id):
    return handle_action(request, listing_id, "close")


def comment(request, listing_id):
    return handle_action(request, listing_id, "comment")


# boilerplate
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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
