"""BGC_Back_End URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from BGC_Back_End import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Graft endpoints
    path("grafts/", views.graft_list),
    path("grafts/<int:id>", views.graft_detail_by_id),
    path("grafts/search/cat/<int:category>", views.graft_detail_by_category),
    path("grafts/search/reg/<int:regulation>", views.graft_detail_by_regulation),
    path("grafts/<int:category>/cat", views.get_cat_name),
    path("grafts/<int:regulation>/reg", views.get_reg_name),
    
    # User / Profile endpoints
    path("users/", views.user_list),
    path("users/<int:id>", views.user_detail_by_id),
    path("users/<str:username>", views.user_detail_by_username),
    path("userByEmail/<str:email>", views.user_detail_by_email),
    
    path("profiles/", views.profile_list),
    path("profiles/<int:user_id>", views.profile_detail_by_user_id),
    path("profilesByBusinessName/<str:business_name>", views.profile_detail_by_business_name),
    
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
