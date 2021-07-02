from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Case, When
from django.contrib.auth import logout
from .recommendation import Recommend
from .forms import RegisterUserForm
from django.contrib import messages
from django.db.models import Q
from .models import *
import pandas as pd
import numpy as np 


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('recommendation:recommended_movies')
    movies = Movie.objects.all()
    query = request.GET.get('q')
    context = {
        'movies':movies
    }
    if query:
        movies = Movie.objects.filter(Q(title__icontains=query)).distinct()
        context = {
            'movies':movies
        }
        return render(request, 'recommendation/index.html', context)
    return render(request, 'recommendation/index.html', context)

# def log_in(request):
#     if request.user.is_authenticated:
# 		return redirect('recommendation:recommended_movies')
# 	else:
#         if request.method == 'POST':
#             username = request.POST['username']
#             password = request.POST['password']
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect("recommendation:recommended_movies")       
#             else:
#                 return render(request, 'recommendation/log_in.html', {'error_message': 'Account Disabled', 'title':'login | MRSystem'})
#         return render(request, 'recommendation/log_in.html', {'title':'login | MRSystem'})


def log_in(request):
	if request.user.is_authenticated:
		return redirect('recommendation:recommended_movies')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('recommendation:recommended_movies')
			else:
				messages.info(request, 'invalid credentials')
		context = {}
		return render(request, 'recommendation/log_in.html', context)

# def sign_up(request):
#     form = RegisterUserForm()
#     context = {
#         'form' : form
#     }
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("recommendation:log_in")
#     return render(request, 'recommendation/sign_up.html', context)




def sign_up(request):
	if request.user.is_authenticated:
		return redirect('recommendation:recommended_movies')
	else:
		form = RegisterUserForm()
		title = 'Sign Up | MRSystem'
		if request.method == 'POST':
			form = RegisterUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account created sucessfully ' + user)
				return redirect('recommendation:log_in')			
		context = {
			'form':form,
			'title': title	
		}
		return render(request, 'recommendation/sign_up.html', context)

def log_out(request):
    logout(request)
    return redirect('recommendation:log_in')

# Redirect to a success page.
@login_required(login_url='recommendation:log_in')
def recommended_movies(request):
    context = {

    }
    return render(request, 'recommendation/recommended_movies.html', context)

# @login_required(login_url='recommendation:log_in')
# def detail(request, movie_id):
#     movie = get_object_or_404(Movie, id=movie_id)
#     if request.method == "POST":
#         rate = request.POST['rating']
#         ratingObject = Rating()
#         ratingObject.user   = request.user
#         ratingObject.movie  = movie
#         ratingObject.rating = rate
#         ratingObject.save()
#         messages.success(request,"Rating submited successfully!")
#         return redirect("recommendation:recommended_movies")
#     return render(request,'recommendation/detail.html', {'movie': movie})

def newuser(request):
	context = {
		'movies':Movie.objects.all()[:16]
	}
	return render(request, 'recommendation/index.html', context)
	

@login_required(login_url='recommendation:log_in')
def detail(request,movie_id):	
	movies = get_object_or_404(Movie,id=movie_id)
	#for rating
	if request.method == "POST":
		rate = request.POST['rating']
		ratingObject = Rating()
		ratingObject.user   = request.user
		ratingObject.movie  = movies
		ratingObject.rating = rate
		ratingObject.save()
		messages.success(request,"Rating submited Successfully!")
		return redirect("recommendation:recommended_movies")
	return render(request,'recommendation/detail.html',{'movies':movies})

@login_required(login_url='recommendation:log_in')
def recommended_movies(request):	
	df=pd.DataFrame(list(Rating.objects.all().values()))
	nu=df.user_id.unique().shape[0]
	current_user_id= request.user.id
	# if new user not rated any movie
	if current_user_id>nu:
		#movie=Movie.objects.get(id=1)
		#q=Rating(user=request.user,movie=movie,rating=5)
		#q.save()
		return redirect("recommendation:newuser")
	print("Current user id: ",current_user_id)
	prediction_matrix,Ymean = Recommend()
	my_predictions = prediction_matrix[:,current_user_id-1]+Ymean.flatten()
	pred_idxs_sorted = np.argsort(my_predictions)
	pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
	pred_idxs_sorted=pred_idxs_sorted+1
	print(pred_idxs_sorted)
	preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
	movie_list=list(Movie.objects.filter(id__in = pred_idxs_sorted,).order_by(preserved)[:10])
	return render(request,'recommendation/recommended_movies.html',{'movie_list':movie_list})
