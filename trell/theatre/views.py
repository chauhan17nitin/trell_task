from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from .models import Movie, Timings, Purchase
# Create your views here.

def index(request):
  if request.user.is_authenticated:
    return redirect('/home/')
  users_count = User.objects.count()
  if users_count > 0:
    login = True
  else:
    login = False
  response = {
    "login": login
  }
  return render(request, "theatre/index.html", response)

def sign_up(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
      user = User.objects.create_user(username=username, password=password)
      user.save()
      auth_login(request, user)
      return redirect('/home/')
    except:
      response = {
        "error": "User Already exists",
        "login": True,
      }
      return render(request, "theatre/index.html", response)



def login(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username = username, password = password)
    if user is not None:
      auth_login(request, user)
      return redirect('/home/')
    response = {
      "error": "INVALID PASSWORD OR USER NOT EXIST",
      "login": True
    }
    user = User.objects.filter(username = username).count()
    return render(request, "theatre/index.html", response)

def logout(request):
  if request.method == "GET":
    logout(request)
    return redirect('/')


def home(request):
  if request.user.is_authenticated:
    movies = Movie.objects.all()
    timings_list = []
    for movie in movies:
      timings = Timings.objects.filter(movie = movie)
      timings_list.append(timings)
    response = {
      "movies": movies,
      "user": request.user,
      "timings": timings_list
    }
    return render(request, "theatre/home.html", response)
  else:
    return redirect('/')


def add_movie(request):
  if request.user.is_authenticated:
    if request.method == "POST":
      movie_name = request.POST.get("movie_name")
      description = request.POST.get("description")
      director = request.POST.get("director")
      duration = request.POST.get("duration")
      try:
        movie = Movie.objects.create(movie_name= movie_name, description = description, director = director, duration = duration)
        movie.save()
        response = {
          "Message": "Movie addition success"
        }
      except Exception as e:
        print("Exception occured", e)
        response = {
          "Message": "Movie already present"
        }

      return redirect('/home/')

def add_timings(request):
  if request.user.is_authenticated:
    if request.method == "POST":
      movie = request.POST.get("movie")
      start_time = request.POST.get("start_time")
      end_time = request.POST.get("end_time")
      number_tickets = request.POST.get("number_tickets")
      movie = Movie.objects.get(id=movie)

      existing_timings = Timings.objects.filter(movie = movie)
      for existing_time in existing_timings:
        if (start_time < existing_time.start_time and end_time > existing_time.start_time) or (start_time > existing_time.start_time and start_time < existing_time.end_time):
          return redirect('/home/')
      time = Timings.objects.create(movie = movie, start_time = start_time, end_time = end_time, tickets_available = number_tickets)
      time.save()
      return redirect('/home/')

def search(request):
  if request.method == "GET":
    name = request.GET.get('name')
    movies = Movie.objects.filter(movie_name__iregex = name, description__iregex = name)

    response = {
      "movies": movies,
      "user": request.user
    }
    return render(request, "theatre/home.html", response)

def purchase_ticket(request, movie_id):
  if request.method == GET:
    movie_id = request.GET.get('movie_id')
    timing_id = request.GET.get('timing_id')

    time = Timings.objects.get(id = timing_id)
    if time.tickets_available > 0:
      time.tickets_available -= 1
      time.save()
      purchase = Purchase.objects.create(user = User.objects.get(request.user), timings = time)
      purchase.save()
      response = {
        "message": "Ticket Booked"
      }
    else:
      response = {
        "message": "Tickets not available"
      }
    return redirect('/home/')











