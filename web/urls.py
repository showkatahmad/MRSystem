from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('war/', war, name = 'war'),
    path('crime/', crime, name = 'crime'),
    path('drama/', drama, name = 'drama'),
    path('family/', family, name = 'family'),
    path('comedy/', comedy, name = 'comedy'),
    path('horror/', horror, name = 'horror'),
    path('action/', action, name = 'action'),
    path('fantasy/', fantasy, name = 'fantasy'),
    path('mystery/', mystery, name = 'mystery'),
    path('romance/', romance, name = 'romance'),
    path('<int:movie_id>/',detail ,name='detail'),
    path('recommend/' , recommend,name='recommend'),
    path('adventure/', adventure, name = 'adventure'),
    path('animation/', animation, name = 'animation'),
    path('biography/', biography, name = 'biography'),
]