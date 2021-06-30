from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *


app_name='recommendation'
urlpatterns = [
    path('', index, name='index'),
    path('login/', log_in, name='log_in'),
    path('logout/', log_out, name='log_out'),
    path('signup/', sign_up, name='sign_up'),
    path('recommendedmovies/', recommended_movies, name='recommended_movies'),
    path('<int:movie_id>/', detail, name='detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)