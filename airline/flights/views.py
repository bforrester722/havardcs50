from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Flight, Passenger
# Create your views here.


def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all()
    })


def book(request, flight_id):
    if request.method == "Post":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse('flight', args=(flight.id)))
