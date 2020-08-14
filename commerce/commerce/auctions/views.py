from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import datetime


from .models import User, Listing

class AddForm(forms.Form):
    name = forms.CharField(max_length=50)
    price = forms.FloatField()
    # image = forms.FileField()

def index(request):
    listing = Listing.objects.all
    return render(request, "auctions/index.html",{
        "listings" : listing
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

def add(request):
    
    if request.method == "POST":
        form = AddForm(request.POST, request.FILES)
        # Check if form data is valid (server-side)       
        if form.is_valid():
            name = form.cleaned_data["name"]
            price = form.cleaned_data["price"]
            image = Post(image=request.FILES['image'])

            # save as dict
            newdata = {
                "name": name,
                "price": price,
                "image" : image
                }

            listing = Listing(name = name, price = price, image = image)
            listing.save()

            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/add.html",
        {
            "message" : "INVALIDED VALUES"
        })

    else:
        return render(request, "auctions/add.html",
        {
            "form" : AddForm()
        })
