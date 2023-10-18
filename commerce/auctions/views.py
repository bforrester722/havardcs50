from datetime import datetime
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import ListingForm
from .models import Bid, Comment, User, Listing, CATEGORY_CHOICES
import logging

logger = logging.getLogger("django")


def get_listings_with_highest_bid(listings):
    for listing in listings:
        bids = listing.bids.all().order_by("bid")
        if bids:
            listing.highest_bid = bids.last().bid
        else:
            listing.highest_bid = listing.startingBid
    return listings


def index(request):
    listings = Listing.objects.filter(closed=False)
    listings = get_listings_with_highest_bid(listings)
    return render(request, "auctions/index.html", {"listings": listings})


def categories(request, category=None):
    listings = Listing.objects.filter(category=category)
    listings = get_listings_with_highest_bid(listings)
    return render(
        request,
        "auctions/categories.html",
        {
            "categories": CATEGORY_CHOICES,
            "category": listings,
        },
    )


def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
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


def watchlist(request):
    user = User.objects.get(pk=int(request.user.id))
    listings = Listing.objects.filter(watchers=user)
    listings = get_listings_with_highest_bid(listings)
    return render(request, "auctions/watchlist.html", {"listings": listings})


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


def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {"form": ListingForm()})


def change_watchlist(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(id=listing_id)
            user = User.objects.get(pk=int(request.user.id))
        except KeyError:
            return HttpResponseBadRequest("Bad Request: no listing chosen")
        except Listing.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: Listing does not exist")
        except User.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: User does not exist")
        if user in listing.watchers.all():
            listing.watchers.remove(user)
        else:
            listing.watchers.add(user)

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def close(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(id=listing_id)
            bids = listing.bids.all()
        except KeyError:
            return HttpResponseBadRequest("Bad Request: no listing chosen")
        except Listing.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: Listing does not exist")
        except User.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: User does not exist")
        listing.closed = True
        listing.winner = bids.last().user
        listing.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def bid(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(id=listing_id)
            bid = request.POST["bid"]
        except KeyError:
            return HttpResponseBadRequest("Bad Request: no listing chosen")
        except Listing.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: Listing does not exist")

        newBid = Bid(listing_id=listing, user=request.user, bid=bid)
        newBid.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def comment(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(id=listing_id)
            comment = request.POST["comment"]
        except KeyError:
            return HttpResponseBadRequest("Bad Request: no listing chosen")
        except Listing.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: Listing does not exist")
        newComment = Comment(
            listing_id=listing,
            user=request.user,
            comment=comment,
            date_time=datetime.now(),
        )
        newComment.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
