from rest_framework import serializers
from django.contrib.auth.models import User
from .models import jobApplication, jobPlatformCred

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = jobApplication
        fields = '__all__'


class PlatformCredSerializer(serializers.ModelSerializer):
    class Meta:
        model = jobPlatformCred
        fields = '__all__'