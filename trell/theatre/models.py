from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
  movie_name = models.CharField(max_length = 100)
  description = models.TextField()
  director = models.CharField(max_length = 100)
  duration = models.TimeField()
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)

class Timings(models.Model):
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
  start_time = models.TimeField()
  end_time = models.TimeField()
  tickets_available = models.IntegerField(default = 0)


class Purchase(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  timings = models.ForeignKey(Timings, on_delete=models.CASCADE)

selcect movie.movie_name, user.username
from movie, user
where user.id = movie.user


samuel@trell.in