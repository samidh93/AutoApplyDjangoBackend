from django.shortcuts import render, redirect
from ..models import jobApplication, jobPlatformCred
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import re
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.views import generic
from django.core import serializers
from ..serializers import ApplicationSerializer, PlatformCredSerializer
from django.views import View
from django.utils.decorators import method_decorator
# Import the FastAPIClient class
from ..fastapi_client import FastAPIClient  
from asgiref.sync import sync_to_async
import logging
logger = logging.getLogger(__name__)

############ Application Views ###########

class ApplicationListView(APIView):
    permission_classes = (IsAuthenticated,)  # Add this line
    def get(self, request):
        applications = jobApplication.objects.all()  # Replace with the appropriate queryset
        # Convert model data to a list of dictionaries
        application_data = []
        for application in applications:
            application_dict = {}
            for field in jobApplication._meta.fields:
                field_name = field.name
                field_value = getattr(application, field_name)
                application_dict[field_name] = field_value
            application_data.append(application_dict)

        context = {'applications': application_data}
        return render(request, 'job_application/application_list.html', context)
