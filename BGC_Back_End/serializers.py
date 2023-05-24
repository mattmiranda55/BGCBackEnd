from rest_framework import serializers
from .models import Graft


class GraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graft
        fields = ['id', 'name', 'description']
