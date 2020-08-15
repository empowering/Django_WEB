# - 이미지 업로드

from django import forms
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import datetime


from .models import *

class AddForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('name', 'price', 'image', 'description', 'category', 'image',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class BiddingForm(forms.ModelForm):
    class Meta:
        model = Bidding
        fields = ('bids',)

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
            form.save()
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

def delete(request, list_id):
    listing = Listing.objects.get(list_id=list_id)
    listing.delete()
    lists = Listing.objects.all
    return render(request, "auctions/index.html",{
        "listings" : lists
    })


def detail(request, list_id):
    content = Listing.objects.get(list_id=list_id)
    bidding = Bidding.objects.filter(item=list_id)
    comment = Comment.objects.all()
    check_comment = comment.filter(post=list_id)

    if check_comment.exists():
        comments = check_comment
    else:
        comments = {}

    # user && form
    user = request.user
    profile = User.objects.get(username=user)
    form = CommentForm()
    bidform = BiddingForm()

    # bids  
    numbids = bidding.count()
    bidslist = Bidding.objects.filter(item=content) # or whatever arbitrary queryset
    maxi = bidslist.aggregate(Max('bids'))['bids__max']
    try :
        maxbidder = Bidding.objects.get(item=content, bids=maxi)
        maxbidder = maxbidder.bidder
    except :
        maxbidder = 0


    if (user == maxbidder):
        curBid = True
    else :
        curBid = False

    return render(request, "auctions/detail.html",{
        "content" : content,
        "profile" : profile,
        "bidding" : bidding,
        "numbids" : numbids,
        "maxi" : maxi,
        "curBid" : curBid,
        "form": form,
        "bidform" : bidform,
        "comments" : comments,
        "maxbidder" : maxbidder
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
    options = dict(OPTIONS)
    
    return render(request, "auctions/category.html",
    {
        "options" : options.values()
    })

def categoryDetail(request, category_name):
    listings = Listing.objects.all().filter(category = category_name.lower())
    return render(request,'auctions/category.html', {
        "category_name" : category_name,
        "listings" : listings
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

@login_required
def bidding(request, list_id):
    post = get_object_or_404(Listing, list_id = list_id)
    userbids = Bidding.objects.filter(item = list_id, bidder=request.user) # 조건 두개 다 맞아야함 
    bidslist = Bidding.objects.filter(item=list_id) # or whatever arbitrary queryset
    maxi = bidslist.aggregate(Max('bids'))['bids__max']

    if request.method == "POST":
        form = BiddingForm(request.POST)
        if form.is_valid():
            maxi = bidslist.aggregate(Max('bids'))['bids__max']

            # maxi error control
            if maxi is None:
                maxi = 0
            
            bidinput = int(form.cleaned_data['bids'])
            if (bidinput > maxi) :

                # 이미 참여했다면 가격 업데이트
                if userbids.exists():
                    bidding = Bidding.objects.get(bidder=request.user, item = list_id)
                    bidding.bids = form.cleaned_data['bids']
                    bidding.save()

                # 참여하지 않았다면 가격 새로 제시
                else :    
                    bids = form.cleaned_data['bids']
                    bidding = Bidding(bids=bids, bidder = request.user, item = post)
                    bidding.save()

    return redirect('detail', list_id=list_id)


