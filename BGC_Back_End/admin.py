from django.contrib import admin
from .models import Graft
from .models import Profile


# Make visible on admin page
admin.site.register(Graft)
admin.site.register(Profile)