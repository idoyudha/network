import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import Error
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Tweet

from datetime import date

def index(request):
    return render(request, "network/index.html")

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
    return HttpResponseRedirect(reverse("index"))

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
@login_required
def tweet(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get contents of email
    data = json.loads(request.body)
    t = data.get("tweet", "")

    # Create one email for each recipient, plus sender
    tweet = Tweet(user_tweet=request.user, tweet_text=t)
    tweet.save()

    return JsonResponse({"message": "Email sent successfully."}, status=201)


def tweet_all(request, user):
    # Get contents of tweet 
    if user == 'home':
        qs = Tweet.objects.all().order_by('-timestamp')
    elif user == request.user.username:
        id = User.objects.values_list('id', flat=True).get(username=user)
        qs = Tweet.objects.filter(user_tweet=id)
    else:
        return JsonResponse({"error": "Invalid page or You're not the user"}, status=400)
    list_tweet = [{"id": i.id, "user":i.user_tweet.username, "tweet": i.tweet_text, "time": i.timestamp.strftime("%b %d, %Y")} for i in qs]
    return JsonResponse(list_tweet, safe=False)

@login_required
def tweet_detail(request, tweet_id):
    try:
        data = Tweet.objects.get(id=tweet_id)
    except:
        raise Http404
    tweet_data = {
        "id": tweet_id,
        "user": data.user_tweet.username,
        "tweet": data.tweet_text
    }
    return JsonResponse(tweet_data)

def profile(request, user):
    user = request.user
    context = {
        user:user
    }
    return render(request, "network/profile.html", context)