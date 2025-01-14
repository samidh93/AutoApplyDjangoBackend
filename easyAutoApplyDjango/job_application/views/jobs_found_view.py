from django.shortcuts import render, redirect
from ..models import *
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
import threading
from ..wix_client import WixClient
logger = logging.getLogger(__name__)

############ Application Views ##########
@method_decorator(csrf_exempt, name='dispatch')
class JobFoundDataView(APIView):
    permission_classes = (IsAuthenticated,)  # Add this line

    def save_to_database(self, request):
        try:
            verified_platform_cred = jobPlatformCred.objects.filter(
                owner_id=request.GET.get('_owner', None), verified=True).latest('created_date')
            # Access 'form-id' inside the 'data' dictionary
            search_params: dict = json.loads(request.GET.get("search_params"))
            logger.info(f"search params : {search_params}, type: {type(search_params)}")
            SearchParamsField = SearchParams(
                job=search_params.get("job"),
                location=search_params.get("location"),
                limit=search_params.get("limit")
            )
            SearchParamsField.save()
            # Access 'form-id' inside the 'data' dictionary
            jobsearch = JobSearch(
                field_id=request.GET.get('_id'),
                search_params=SearchParamsField,
                user=verified_platform_cred
            )
            jobsearch.save()
            logger.info("job application  saved properly")
            return {"message": 'success saving job application ', "job_search": jobsearch}
        except Exception as e:
            logger.error(f"error saving job application {str(e)}")
            return {"message": 'error saving job application ', "error": str(e)}

    ############## Search jobs ##############
    def fastapiGetJobsFound(self, jobsearch: JobSearch):  # after search
        try:
            # Create an instance of the FastAPIClient with the base URL of your FastAPI app
            fastapi_client = FastAPIClient()  # Replace with your FastAPI URL
            # Use the FastAPIClient to send the data to the FastAPI endpoint asynchronously
            forward_request = {
                "user":
                {
                    "email": jobsearch.user.email,
                    "password": jobsearch.user.password,
                    "platform": jobsearch.user.platform,
                    "owner": jobsearch.user.owner_id,
                    "field_id": jobsearch.user.field_id,
                    "created_date": jobsearch.user.created_date
                },
                "search_params":
                {
                    "job": jobsearch.search_params.job,
                    "location": jobsearch.search_params.location,
                    "limit": str(jobsearch.search_params.limit),
                },
                "field_id": jobsearch.field_id  # added to retrieve field in jobsesrch collection
            }
            response_data = fastapi_client.getJobsFoundAfterSearch(forward_request)
            #logger.info("response: %s", response_data)
           # forward resp to wix
            wixClientCred = WixClient()
            if response_data["status"] == 'ok':  # success
                # save job count to data: add job count to jobApplication
                # data.save()  # Save the changes to the database
                #logger.info("response fast api: %s ", response_data)
                wixClientCred.putJobsFoundCountResp(response_data)
                return response_data
            else:
                logger.error(
                    f"error with login data {response_data['status_code']}")
                wixClientCred.putJobsFoundCountResp(response_data)
                return {"message": 'error with login data ', "error": response_data["status_code"]}
        except Exception as e:
            logger.error(f"error sending request to FastAPI server {str(e)}")
            return {"message": 'error sending request to FastAPI server ', "error": str(e)}

    ############## get found jobs ##############
    def get(self, request):
        try:
            logger.info(f"request: {request}")
            database_response = self.save_to_database(request)
            # Check if there was an error in saving to the database
            if 'error' in database_response:
                return JsonResponse({'error': database_response}, status=400)
            forward_thread = threading.Thread(
                target=self.fastapiGetJobsFound, args=[database_response["job_search"]])
            forward_thread.start()
            # Respond immediately
            return JsonResponse({'message': 'job search count started', "status": 202}, status=202)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in the request', "status": 400}, status=400)
