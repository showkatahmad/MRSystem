from django.db import models

# Create your models here.

class Genre(models.Model):
    title = models.CharField(max_length=64, null=True)
    def __str__(self):
        return self.title

class Movie(models.Model):
    title = models.CharField(max_length=128, null=True)
    poster = models.ImageField(upload_to='movie_poster')
    genre = models.ManyToManyField(Genre)
    def __str__(self):
        return self.title

