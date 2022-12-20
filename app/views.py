from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json

from django.contrib.auth import logout, authenticate, login
from .models import *


def home(request):
    events = Event.objects.all().order_by('date', 'time')
    print(request.user.username)
    liked_events = []

    if request.user.is_authenticated:
        custom_user_object = CustomUser.objects.get(user=request.user)
        liked = custom_user_object.liked_events.all()
        print(liked)
        for liked_event in liked:
            liked_events.append(liked_event.id)
        print(liked_events)
    return render(request, 'app/home.html', {'events': events, 'liked': liked_events, 'message': 'All Events'})


def login_view(request):
    if request.method == 'GET':
        return render(request, 'app/login.html')
    else:
        username = request.POST['username']
        password = request.POST.get('password')
        print(username, password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect(reverse('home'))
        else:
            return HttpResponse("<h3>Invalid userename or password</h3>")


def signup(request):
    if request.method == 'GET':
        return render(request, "app/signup.html")
    else:
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            return HttpResponse("<h3>Passwords should be same!</h3>")

        # Check whether a user exists with the same username!

        user = User.objects.filter(username=username)

        if len(user) != 0:
            return HttpResponse(f"<h3>{username}: This username has already been taken! Please use another username")

        new_user = User.objects.create_user(
            username=username, password=password1)
        new_user.save()

        new_custom_user = CustomUser.objects.create(user=new_user)
        new_custom_user.save()

        login(request, new_user)

        return redirect(reverse('home'))


def create_event(request):
    if request.method == "GET":
        return render(request, "app/create_event.html")
    else:
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        date = request.POST.get("date")
        time = request.POST.get("time")
        location = request.POST.get("location")

        new_event = Event()
        new_event.title = title
        new_event.description = description
        new_event.date = date
        new_event.time = time
        new_event.location = location
        new_event.image = image
        new_event.save()
        return redirect(reverse('home'))


def logout_view(request):
    logout(request)
    return redirect(reverse('home'))


def liked_events(request):
    events = Event.objects.all()
    custom_user_object = CustomUser.objects.get(user=request.user)
    liked = custom_user_object.liked_events.all()
    liked_events = []

    for event in liked:
        liked_events.append(event.id)
    print(liked, liked_events)

    return render(request, 'app/home.html', {'events': liked, 'liked': liked_events, 'message': 'Liked Events'})


def clicked(request):
    print(request.POST.get("id"))
    event_id = int(request.POST.get("id"))
    event = Event.objects.get(id=event_id)
    custom_user_object = CustomUser.objects.get(user=request.user)
    liked = custom_user_object.liked_events.all()

    if request.is_ajax():
        if event not in liked:
            custom_user_object.liked_events.add(event)
            custom_user_object.save()

            response = {
                'success': 'liked'
            }

            return JsonResponse(response)
        else:
            custom_user_object.liked_events.remove(event)
            custom_user_object.save()

            response = {
                'success': 'unliked'
            }

            return JsonResponse(response)

    return redirect(reverse("home"))
