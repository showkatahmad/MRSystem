from django.urls import path
from .views import *

from django.urls import path, include
urlpatterns = [
    path('',  index, name='index'),
	path('signup/', signup, name="signup"),
	path('signin/', signin, name="signin"),  
	path('signout/', signout, name="signout"),
	
	path('profile/', profile, name="profile")

	
	# path('search', search, name="search"),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)