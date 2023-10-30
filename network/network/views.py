
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.db.models import Count
from django.http import  HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import User, Post, Like
import logging
logger = logging.getLogger("django")


class PostForm(forms.Form):
    text = forms.CharField(
        label="",
        max_length=280,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
    )


def index(request):
    allPosts = (
        Post.objects.annotate(like_count=Count("like")).order_by("-date_time").all()
    )
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data["text"]
            post = Post(user=request.user, text=text)
            post.save()
            return HttpResponseRedirect(reverse("index"))

    posts = paginate(request, allPosts)
    return render(request, "network/index.html", {"form": PostForm(), "posts": posts})

# Filter posts that the user is following
@login_required
def following(request):
    user = request.user  
    logger.info(Post.objects.filter(user__in=user.following.all()))
    
    following_posts = (
        Post.objects.filter(user__in=user.following.all())
        .annotate(like_count=Count("like"))
        .order_by("-date_time")
    )
    posts = paginate(request, following_posts)
    return render(request, "network/index.html", {"posts": posts})

# builds data for displaying profile section
def profile(request, user):
    user = get_object_or_404(User, username=user)
    user.date_joined = user.date_joined.strftime('%b. %d, %Y')
    num_followers = user.followers.count()
    num_following = user.following.count()
    userPosts = Post.objects.filter(user=user).order_by("-date_time")
    posts = paginate(request, userPosts)
    if request.user.is_authenticated:
        following = user in request.user.following.all()
    else:
        following = False
    
    context = {
        "current_user": user,
        "num_followers": num_followers,
        "num_following": num_following,
        "posts": posts,
        "following": following,
        "is_profile_page": True,
    }
    
    return render(request, "network/index.html", context)

# function to handle pagination
def paginate(request, posts):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = paginator.page(1)
        logger.error(posts)
    except EmptyPage:
        # If page is out of range, deliver the last page
        posts = paginator.page(paginator.num_pages)
    return posts

# saves when post is edited 
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        new_content = request.POST.get("edited_content")
        if request.user == post.user:
            post.text = new_content
            post.save()
            return JsonResponse({"success": True, "updated_text": post.text})
        else:
            return JsonResponse({"success": False, "error": "Permission denied"})

    return JsonResponse({"success": False, "error": "Invalid request method"})


# checks if user is following and follow or unfollows
@login_required
def toggle_follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    current_user = request.user
    if user_to_follow in current_user.following.all():
        current_user.following.remove(user_to_follow)
    else:
        current_user.following.add(user_to_follow)

    return HttpResponseRedirect(reverse("profile", args=(user_to_follow.username,)))

# Check if the user has already liked the post and likes or unlikes
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    like, created = Like.objects.get_or_create(user=user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    # Update the like count for the post
    like_count = post.like_set.count()  

    return JsonResponse({"liked": liked, "like_count": like_count})

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
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
