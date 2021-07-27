import numpy as np 
import pandas as pd
from .models import *
from django.db.models import Q
from django.http import Http404
from django.contrib import messages
from django.db.models import Case, When
from .recommendation import Myrecommend
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required


# for recommendation
@login_required
def recommend(request):	
	df=pd.DataFrame(list(Myrating.objects.all().values()))
	nu=df.user_id.unique().shape[0]
	current_user_id= request.user.id
	# if new user not rated any movie
	if current_user_id>nu:
		movie=Movie.objects.get(id=15)
		q=Myrating(user=request.user,movie=movie,rating=0)
		q.save()

	print("Current user id: ",current_user_id)
	prediction_matrix,Ymean = Myrecommend()
	my_predictions = prediction_matrix[:,current_user_id-1]+Ymean.flatten()
	pred_idxs_sorted = np.argsort(my_predictions)
	pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
	pred_idxs_sorted=pred_idxs_sorted+1
	print(pred_idxs_sorted)
	preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
	movie_list=list(Movie.objects.filter(id__in = pred_idxs_sorted,).order_by(preserved)[:32])
	return render(request,'web/recommend.html',{'movie_list':movie_list, 'active_recommend': 'active'})


# List view
def index(request):
	movies = Movie.objects.all()[:54]
	query  = request.GET.get('q')
	if query:
		movies = Movie.objects.filter(Q(title__icontains=query)).distinct()
		return render(request,'web/list.html',{'movies':movies})
	return render(request,'web/list.html',{'movies':movies, 'active_all': 'active' })


# detail view
@login_required
def detail(request,movie_id):
	if not request.user.is_authenticated:
		return redirect("login")
	if not request.user.is_active:
		raise Http404
	movies = get_object_or_404(Movie,id=movie_id)
	#for rating
	if request.method == "POST":
		rate = request.POST['rating']
		ratingObject = Myrating()
		ratingObject.user   = request.user
		ratingObject.movie  = movies
		ratingObject.rating = rate
		ratingObject.save()
		messages.success(request,"Your Rating is submited ")
		return redirect("index")
	return render(request,'web/detail.html',{'movies':movies})

			
def action(request):
    context = {
        'genre': Genre.objects.filter(genre='action')[:18],
        'active_action': 'active'
    }    
    return render(request, 'web/genre.html', context)


def adventure(request):
    context = {
        'genre': Genre.objects.filter(genre='adventure')[:18],
        'active_adventure': 'active'
    }
    return render(request, 'web/genre.html', context)


def animation(request):
    context = {
        'genre': Genre.objects.filter(genre='animation')[:18],
        'active_animation': 'active'
    }
    return render(request, 'web/genre.html', context)


def biography(request):
    context = {
        'genre': Genre.objects.filter(genre='biography')[:18],
        'active_biography': 'active'
    }
    return render(request, 'web/genre.html', context)


def comedy(request):
    context = {
        'genre': Genre.objects.filter(genre='comedy')[:18],
        'active_comedy': 'active'
    }
    return render(request, 'web/genre.html', context)


def crime(request):
    context = {
        'genre': Genre.objects.filter(genre='crime')[:18],
        'active_crime': 'active'
    }
    return render(request, 'web/genre.html', context)


def drama(request):
    context = {
        'genre': Genre.objects.filter(genre='drama')[:18],
        'active_drama': 'active'
    }
    return render(request, 'web/genre.html', context)


def family(request):
    context = {
        'genre': Genre.objects.filter(genre='family')[:18],
        'active_family': 'active'
    }
    return render(request, 'web/genre.html', context)


def fantasy(request):
    context = {
        'genre': Genre.objects.filter(genre='fantasy')[:18],
        'active_fantasy': 'active'
    }
    return render(request, 'web/genre.html', context)


def horror(request):
    context = {
        'genre': Genre.objects.filter(genre='horror')[:18],
        'active_horror': 'active'
    }
    return render(request, 'web/genre.html', context)


def mystery(request):
    context = {
        'genre': Genre.objects.filter(genre='mystery')[:18],
        'active_mystery': 'active'
    }
    return render(request, 'web/genre.html', context)


def romance(request):
    context = {
        'genre': Genre.objects.filter(genre='romance')[:18],
        'active_romance': 'active'
    }
    return render(request, 'web/genre.html', context)


def war(request):
    context = {
        'genre': Genre.objects.filter(genre='war')[:18],
        'active_war': 'active'
    }
    return render(request, 'web/genre.html', context)





