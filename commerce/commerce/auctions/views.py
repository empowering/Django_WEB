from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import datetime


from .models import *

OPTIONS = (
    ('clothing','Clothing'),
    ('crafts','Crafts'),
    ('home','Home'), 
    ('pet','Pet'), 
)


class AddForm(forms.Form):
    name = forms.CharField(max_length=50)
    price = forms.FloatField()
    description = forms.CharField(max_length=100)
    category = forms.ChoiceField(required=True, choices=OPTIONS)
    # image = forms.FileField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

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
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            # image = Post(image=request.FILES['image'])

            listing = Listing(name = name, price = price, author = request.user, description = description,
                category = category)
            # , image = image)
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

def detail(request, list_id):
    content = Listing.objects.get(list_id=list_id)
    comment = Comment.objects.all()
    check_comment = comment.filter(post=list_id)

    if check_comment.exists():
        comments = check_comment
    else:
        comments = {}

    user = request.user
    profile = User.objects.get(username=user)
    form = CommentForm()

    return render(request, "auctions/detail.html",{
        "content" : content,
        "profile" : profile,
        "form": form,
        "comments" : comments
    })


@login_required
def post_like_toggle(request, list_id):
    post = Listing.objects.get(list_id=list_id)
    user = request.user
    profile = User.objects.get(username=user)

    check_watchlist = profile.watchlist.filter(list_id=list_id)

    if check_watchlist.exists():
        profile.watchlist.remove(post)
        post.likes -= 1
        post.save()
    else:
        profile.watchlist.add(post)
        post.likes += 1
        post.save()

    return redirect('detail', list_id)

@login_required
def watchlist(request):
    user = request.user
    profile = User.objects.get(username=user)

    return render(request, "auctions/watchlist.html"
    ,{
        "profile" : profile
    })

def category(request):
    options = list(OPTIONS)
    
    for opt in options :
        opt = list(opt)
    
    return render(request, "auctions/category.html",
    {
        "options" : options
    })

@login_required
def comment(request, list_id):
    post = get_object_or_404(Listing, list_id = list_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            comment = Comment(text=text)
            comment.author = request.user
            comment.post = post
            comment.save()
        return redirect('detail', list_id=list_id)
