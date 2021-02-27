import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import Error
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Tweet, Profile

from datetime import date

def index(request):
    # Create one tweet 
    if request.method == "POST":
        t = request.POST["tweet_text"]
        Tweet.objects.create(user_tweet=request.user, tweet_text=t)
        return HttpResponseRedirect('/')
    else:
        list_user = User.objects.values_list('username', flat=True).exclude(username=request.user)
        # Get data from query
        qs = Tweet.objects.all().order_by('-timestamp')
        paginator = Paginator(qs, 10)

        page_number = request.GET.get('page') # split query for every page
        page_obj = paginator.get_page(page_number)
        context = {
            "list_user": list_user,
            "page_obj": page_obj
        }
        return render(request, "network/index.html", context)

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required(login_url='/login/')
def tweet(request):
    # Composing a new tweet must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get contents of tweet
    data = json.loads(request.body)
    t = data.get("tweet", "")

    # Create one tweet for each recipient, plus sender
    tweet = Tweet(user_tweet=request.user, tweet_text=t)
    tweet.save()

    return render(request, "network/index.html")

@csrf_exempt
@login_required(login_url='/login/')
def tweet_id(request, pk):
    qs = Tweet.objects.filter(id=pk)
    # Return tweets via GET
    if request.method == 'GET':
        list_tweet = [{"id": i.id, "user":i.user_tweet.username, "tweet": i.tweet_text, "time": i.timestamp.strftime("%b %d, %Y"), "likes": list(i.likes.values_list('username', flat=True)) } for i in qs]
        return JsonResponse(list_tweet, safe=False)
    # Update edited tweet
    elif request.method == 'PUT':
        tweet = Tweet.objects.get(id=pk)
        data = json.loads(request.body)
        user = request.user.id
        if data.get("tweet") is not None:
            tweet.tweet_text = data["tweet"]
        if data.get("likes") is not None:
            if data["likes"] is True:
                tweet.likes.add(user)
            else:
                tweet.likes.remove(user)
        tweet.save()
        return JsonResponse({"message": "Tweet edited or liked successfully."}, status=201)
    # Tweet must be via GET or PUT
    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)

@login_required(login_url='/login/')
def tweet_all(request, user):
    list_user = User.objects.values_list('username', flat=True)
    # Get data for following tweets
    data = Profile.objects.values_list('following', flat=True).filter(id=request.user.id)
    # Get contents of tweet 
    if user == 'home':
        qs = Tweet.objects.all().order_by('-timestamp')
    elif user =='following':
        following = Profile.objects.values_list('following', flat=True).filter(id=1)
        qs = Tweet.objects.filter(user_tweet__in=following)
    elif user in list_user:
        id = User.objects.values_list('id', flat=True).get(username=user)
        qs = Tweet.objects.filter(user_tweet=id).order_by('-timestamp')
    else:
        return JsonResponse({"error": "Invalid page or You're not the user"}, status=400)
    list_tweet = [{"id": i.id, "user":i.user_tweet.username, "tweet": i.tweet_text, "time": i.timestamp.strftime("%b %d, %Y")} for i in qs]
    return JsonResponse(list_tweet, safe=False)

@login_required(login_url='/login/')
def profile(request, user_profile):
    list_user = User.objects.values_list('username', flat=True).exclude(username=request.user)
    check_user = User.objects.values_list('username', flat=True)
    id = User.objects.values_list('id', flat=True).get(username=user_profile)
    id_login = User.objects.values_list('id', flat=True).get(username=request.user)
    profile = Profile.objects.filter(username=id)
    follow = Profile.objects.filter(following=id).count()

    # Check if user is already follow
    follow_data = Profile.objects.values_list('following', flat=True).filter(username=id_login)

    # Get data from query
    id = User.objects.values_list('id', flat=True).get(username=user_profile)
    qs = Tweet.objects.filter(user_tweet=id).order_by('-timestamp')
    paginator = Paginator(qs, 10)

    page_number = request.GET.get('page') # split query for every page
    page_obj = paginator.get_page(page_number)
    
    if user_profile in check_user:
        context = {
            "list_user": list_user,
            "username": user_profile,
            "id": id,
            "profile": profile,
            "follow": follow,
            "follow_data": follow_data,
            "page_obj": page_obj
        }
        return render(request, "network/profile.html", context)
    else:
        return JsonResponse({"error": "Profile not found."}, status=404)

@csrf_exempt
@login_required(login_url='/login/')
def following(request, user_profile):
    id = User.objects.values_list('id', flat=True).get(username=user_profile)
    user_id = request.user.id
    obj = Profile.objects.get(username=user_id)
    obj.following.add(id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
@login_required(login_url='/login/')
def unfollow(request, user_profile):
    id = User.objects.values_list('id', flat=True).get(username=user_profile)
    user_id = request.user.id
    obj = Profile.objects.get(username=user_id)
    obj.following.remove(id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login/')
def tweet_following(request):
    list_user = User.objects.values_list('username', flat=True).exclude(username=request.user)
    # Get data from query
    following = Profile.objects.values_list('following', flat=True).filter(id=request.user.id)
    qs = Tweet.objects.filter(user_tweet__in=following).order_by('-timestamp')
    paginator = Paginator(qs, 10)

    page_number = request.GET.get('page') # split query for every page
    page_obj = paginator.get_page(page_number)
    context = {
        "list_user": list_user,
        "page_obj": page_obj
    }
    return render(request, "network/following.html", context)
