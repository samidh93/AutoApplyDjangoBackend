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
from ..wix_client import WixClient
import threading
from .jobs_search_view import JobSearchDataView
import logging
logger = logging.getLogger(__name__)

############ Application Views ###########
@method_decorator(csrf_exempt, name='dispatch')
class JobSearchedDataView(JobSearchDataView):
    permission_classes = (IsAuthenticated,)  # Add this line

    ############## get searched jobs ##############
    def fastapiGetSearchedJobs(self, data: jobApplication):
        try:
            # Create an instance of the FastAPIClient with the base URL of your FastAPI app
            fastapi_client = FastAPIClient()  # Replace with your FastAPI URL
            # Use the FastAPIClient to send the data to the FastAPI endpoint asynchronously
            forward_request = {
                "user":
                {
                    "email": data.platform_cred.email,
                    "password": data.platform_cred.password,
                    "platform": data.platform_cred.platform,
                    "owner": data.platform_cred.owner_id,
                    "field_id": data.platform_cred.field_id,
                    "created_date": data.platform_cred.created_date
                },
                "search_params":
                {
                    "job": data.job_title,
                    "location": data.job_location,
                    "limit": data.limit,
                },
                "field_id": data.field_id  # added to retrieve field in jobsesrch collection
            }   
            
            response_data = fastapi_client.getJobsFoundAfterSearch(data)
            #logger.info("response: %s", response_data)
            return response_data
        except Exception as E:
            logger.error(str(E))
            raise

    def get(self, request):
        try:
            logger.info("body: %s", json.loads(request.body))
            # save the incoming req data in db and rreturn obj
            database_response, database_obj = self.save_to_database(request)
          # Check if there was an error in saving to the database
            if 'error' in database_response:
                return JsonResponse({'error': database_response}, status=400)
            fastapi_response_json = self.fastapiGetSearchedJobs(database_obj)
            # Check if there was an error in saving to the database
            # Respond immediately
            return JsonResponse({'message': 'job search count started', "status": 202}, status=202)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in the request', "status": 400}, status=400)
