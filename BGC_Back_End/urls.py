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
from django.urls import path, include
from BGC_Back_End import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Graft endpoints
    path("grafts/", views.graft_list),
    path("grafts/<int:id>", views.graft_detail_by_id),
    path("grafts/<str:name>", views.graft_detail_by_name),
    path("grafts/search/cat/<int:category>", views.graft_detail_by_category),
    path("grafts/search/reg/<int:regulation>", views.graft_detail_by_regulation),
    path("grafts/<int:category>/cat", views.get_cat_name),
    path("grafts/<int:regulation>/reg", views.get_reg_name),
    path("grafts/<int:id>/img", views.upload_image),
    path("grafts/search/user", views.graft_detail_by_username),
    path("grafts/validate", views.validate_graft),
    path("grafts/imageupload", views.upload_image),
    path("grafts/documentupload", views.upload_document),
    
    
    # User / Profile endpoints
    path("users/", views.user_list),
    path("users/<int:id>", views.user_detail_by_id),
    path("users/<str:username>", views.user_detail_by_username),
    path("userByEmail/<str:email>", views.user_detail_by_email),
    
    # User Auth endpoints
    # use /users/ to POST new users 
    path("users/login/", views.loginUser),
    path("users/info/", views.userInfo),
    path("users/logout/", views.logout),
    path("users/postgraft/", views.user_post_graft),
    path("users/deletegraft/", views.user_delete_graft),
    path("users/changepassword/", views.change_password),
    path("users/changeusername/", views.change_username),
    
    path("profiles/", views.profile_list),
    path("profiles/<int:user_id>", views.profile_detail_by_user_id),
    path("profilesByBusinessName/<str:business_name>", views.profile_detail_by_business_name),

#     path("pricing/purchase", views.user_purchase_credits),
#     path("pricing/purchase/single", views.payment_form_single),
    
    
#    # PayPal endpoints
#    path('paypal/', include('paypal.standard.ipn.urls')),
#    path('payment-completed', views.payment_completed),
#    path('payment-failed', views.payment_failed)
    
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
