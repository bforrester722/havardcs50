from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from .forms import ListingForm
from .models import User, Listing


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def categories(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Flight not found.")
    return render(request, "auctions/listing.html", {
        "listing": listing,

    })


def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def listings(request):
    return render(request, "auctions/listings.html", {
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


def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            imgUrl = form.cleaned_data["imgUrl"]
            startingBid = form.cleaned_data["startingBid"]
            title = form.cleaned_data["title"]

            passenger = Listing.objects.get(
                pk=int(request.POST["passenger"]))
            flight = Flight.objects.get(pk=flight_id)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {"form": ListingForm()})
