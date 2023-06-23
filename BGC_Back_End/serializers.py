from rest_framework import serializers
from .models import *


class GraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graft
        fields = ['id', 'name', 'description', 'category', 'regulation', 'created_at', 'image', 'purchase_link']


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
