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
from ..wix_client import WixClient
import threading
import logging
logger = logging.getLogger(__name__)

############ Application Views ###########


@method_decorator(csrf_exempt, name='dispatch')
class JobSearchDataView(APIView):
    permission_classes = (IsAuthenticated,)  # Add this line

    def save_to_database(self, request):
        try:
            data: dict = json.loads(request.body)
            verified_platform_cred = jobPlatformCred.objects.filter(
                owner_id=data['_owner'], verified=True).latest('created_date')

            search_params: dict = data.get("search_params")
            SearchParamsField = SearchParams(
                job=search_params.get("job"),
                location=search_params.get("location"),
                limit=search_params.get("limit")
            )
            SearchParamsField.save()
            # Access 'form-id' inside the 'data' dictionary
            jobsearch = JobSearch(
                field_id=data['_id'],
                search_params=SearchParamsField,
                user=verified_platform_cred
            )
            jobsearch.save()
            logger.info("job application data saved properly")
            return {"message": 'success saving job application  ', "job_search":jobsearch}
        except Exception as e:
            logger.error(f"error saving job application  {str(e)}")
            return {"message": 'error saving job application ', "error": str(e)}

    ############## Search jobs ##############
    def fastapiSearchJobs(self, jobsearch: JobSearch):
        try:
            # Create an instance of the FastAPIClient with the base URL of your FastAPI app
            fastapi_client = FastAPIClient()  # Replace with your FastAPI URL
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
            # Use the FastAPIClient to send the data to the FastAPI endpoint asynchronously
            response_data = fastapi_client.searchJobs(forward_request)
            #logger.info("response: %s", response_data)
            wixClientCred = WixClient()
            if response_data["status"] == 'ok':  # success
                # save job count to data: add job count to jobApplication
                # data.save()  # Save the changes to the database
                #logger.info("response fast api: %s ", response_data)
                wixClientCred.putJobsSearchResp(response_data)
                return response_data
            else:
                logger.error(
                    f"error with login data {response_data['status_code']}")
                wixClientCred.putJobsSearchResp(response_data)
                return {"message": 'error with login data ', "error": response_data["status_code"]}
        except Exception as e:
            logger.error(f"error sending request to FastAPI server {str(e)}")
            return {"message": 'error sending request to FastAPI server ', "error": str(e)}

    def post(self, request):
        try:
            logger.info("body: %s", json.loads(request.body))
            # save the incoming req data in db and rreturn obj
            database_response = self.save_to_database(request)
            # create req data and forward it, return the resp
            if 'error' in database_response:
                return JsonResponse({'error': database_response}, status=400)
            forward_thread = threading.Thread(
                target=self.fastapiSearchJobs, args=[database_response["job_search"]])
            forward_thread.start()
            # Respond immediately
            return JsonResponse({'message': 'job search started', "status": 202}, status=202)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in the request', "status": 400}, status=400)
