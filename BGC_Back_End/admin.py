from django.contrib import admin
from .models import Graft
from .models import Profile
from .models import Regulation
from .models import Category


# Make visible on admin page
admin.site.register(Graft)
admin.site.register(Profile)
admin.site.register(Regulation)
admin.site.register(Category)