
from django.shortcuts import render, redirect
from ..models import jobApplication, jobPlatformCred
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import asyncio
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.views import generic
from django.core import serializers
from ..serializers import ApplicationSerializer, PlatformCredSerializer
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
# Import the FastAPIClient class
from ..fastapi_client import FastAPIClient
from ..wix_client import WixClient 
from asgiref.sync import sync_to_async
import logging
logger = logging.getLogger(__name__)
import threading
########### Platform Views ############

@method_decorator(csrf_exempt, name='dispatch')
class VerifyPlatformCredDataView(APIView):
    permission_classes = (IsAuthenticated,)

    def save_to_database(self, data: dict):
        try:
            # Create a new jobPlatformCred instance
            job_platform_cred = jobPlatformCred(
                # id auto incremented
                field_id=data.get('_id'),
                owner_id=data.get('_owner'),
                platform=data.get('title'),
                email=data.get('email'),
                password=data.get('password'),
                created_date=data.get('_createdDate'),
                updated_date=data.get('_updatedDate', ""),
                verified=data.get('verified') ,
                cookies=data.get('cookies', ""),
            )
            # Save the instance to the Django database
            job_platform_cred.save()
            logger.info("platform data saved properly")
            return {"message": 'success saving platform cred '}, job_platform_cred
        except Exception as e:
            logger.error(f"error saving platform cred {str(e)}")
            return {"message": 'error saving platform cred ', "error": str(e)}

    def forward_to_fastapi(self, data: jobPlatformCred):
        try:
            # Create an instance of the FastAPIClient with the base URL of your FastAPI app
            fastapi_client = FastAPIClient()  # Replace with your FastAPI URL
            #data expected by fastapi
            forward_request = {
                "user": {
                    "owner": data.owner_id,
                    "platform": data.platform,
                    "email": data.email,
                    "password": data.password,
                    "field_id": data.field_id,
                    "created_date": data.created_date
                }
            }
            response_data = fastapi_client.verifyPlatformCred(forward_request)
            logger.info(f"response data fastapi: {response_data}")
            # forward resp to wix
            wixClientCred = WixClient()
            if response_data["status_code"] == 200:  # success
                data.verified = response_data["data"]["data"]["verified"]
                data.cookies = response_data["data"]["data"]["cookies"]
                data.save()  # Save the changes to the database
                #logger.info("response fast api: %s ", response_data)
                wixClientCred.putPlatformCredResp(response_data)
                return response_data
            else:
                logger.error(f"error with login data {response_data['status_code']}")
                wixClientCred.putPlatformCredResp(response_data)
                return {"message": 'error with login data ', "error": response_data["status_code"]}     
        except Exception as e:
            logger.error(f"error sending request to FastAPI server {str(e)}")
            return {"message": 'error sending request to FastAPI server ', "error": str(e)}

    def post(self, request):
        try:
            logger.info(f"request: {request.body}")
            data = json.loads(request.body)
            # Step 1: Save data to the Django database
            database_response, database_obj = self.save_to_database(data)
            # Check if there was an error in saving to the database
            if 'error' in database_response:
                return JsonResponse({'error': database_response}, status=400)
            # Step 2: Forward the request to FastAPI asynchronously
            forward_thread = threading.Thread(target=self.forward_to_fastapi,args=[database_obj] )
            forward_thread.start()
            
            # Respond immediately
            return JsonResponse({'message': 'platform cred verification started', "status": 202}, status=202)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in the request', "status": 400}, status=400)