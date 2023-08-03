from rest_framework import serializers
from .models import *


class GraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graft
        fields = ['id', 'name', 'description', 'category', 'regulation', 'image', 'price', 'purchase_link', 'created_by', 'documents', 'validated']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class RegulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regulation
        fields = ['id', 'name']




"""

User / Profile Serializers 


"""

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_id', 'num_credits', 'business_name', 'phone_number']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
