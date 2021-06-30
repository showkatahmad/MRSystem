from django.contrib import admin
from .models import *

from .models import Profile
# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(Profile)