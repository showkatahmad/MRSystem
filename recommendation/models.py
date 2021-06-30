from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.
class Genre(models.Model):
    title = models.CharField(max_length=64, null=True)
    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=64, null=True)
    poster = models.ImageField(upload_to='images/')
    genre = models.ManyToManyField(Genre)
    def __str__(self):
        return self.title


class Rating(models.Model):
	user   	= models.ForeignKey(User, on_delete=models.CASCADE) 
	movie 	= models.ForeignKey(Movie, on_delete=models.CASCADE)
	rating 	= models.IntegerField(default=1, validators=[MaxValueValidator(5),MinValueValidator(0)])