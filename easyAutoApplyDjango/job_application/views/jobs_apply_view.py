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
from ..wix_client import WixClient
from asgiref.sync import sync_to_async
from .utils import generate_download_resume_link
import threading
import logging
logger = logging.getLogger(__name__)

########### Jobs Views ############


class JobApplyDataView(APIView):
    permission_classes = (IsAuthenticated,)

    ##### create candidate ####
    def save_to_database(self, request):
        try:
            # Assuming you have incoming JSON data in the request
            data = json.loads(request.body)

            # Create Address instance
            address_data = data["candidate"]["address"]
            address = Address.objects.create(
                street_name=address_data["street_name"],
                street_number=address_data["street_number"],
                city=address_data["city"],
                zip=address_data["zip"],
                country=address_data["country"]
            )
            address.save()

            # Create Skills
            skills_data = data["candidate"]["skills"]
            languages = skills_data["languages"]
            softwares = skills_data["softwares"]

            langs = []
            for lang in languages:
                langObj = Language.objects.create(
                    name=lang["title"],
                    proficiency=lang["level"]
                )
                langObj.save()
                langs.append(langObj)

            softs = []
            for soft in softwares:
                softObj = Software.objects.create(
                    name=soft["title"],
                    proficiency=soft["level"]
                )
                softObj.save()
                softs.append(softObj)

            skills = Skill.objects.create()
            skills.softwares.set(softs)
            skills.languages.set(langs)
            skills.save()

            # Create Experiences
            experience_data = data["candidate"]["experiences"]
            experiences = []

            for exp_data in experience_data:
                experience = Experience.objects.create(
                    job_title=exp_data["title"],
                    company=exp_data["company"],
                    duration=exp_data["from"] + ' to ' + exp_data["to"]
                )
                experience.save()
                experiences.append(experience)

            # Create Educations
            education_data = data["candidate"]["educations"]
            educations = []

            for edu_data in education_data:
                education = Education.objects.create(
                    degree=edu_data["title"],
                    university=edu_data["institution"],
                    duration=edu_data["from"] + ' to ' + edu_data["to"]
                )
                education.save()
                educations.append(education)

            # Create Candidate
            candidate_data = data["candidate"]
            candidate = Candidate.objects.create(
                firstname=candidate_data["firstname"],
                lastname=candidate_data["lastname"],
                gender=candidate_data["gender"],
                resume=generate_download_resume_link(candidate_data["resume"]),
                phone_number=candidate_data["phone_number"],
                start_date=candidate_data["start_date"],
                address=address,
                limit=candidate_data["limit"],
                visa_required=candidate_data["visa_required"],
                years_experience=candidate_data["years_experience"],
                desired_salary=candidate_data["desired_salary"],
                skills=skills,
            )
            candidate.experiences.set(experiences)
            candidate.educations.set(educations)
            candidate.save()

            # Create SearchParams
            search_params_data = data["search_params"]
            search_params = SearchParams.objects.create(
                job=search_params_data["job"],
                location=search_params_data["location"],
                limit=search_params_data["limit"]
            )
            search_params.save()

            # Create JobApply
            verified_platform_cred = jobPlatformCred.objects.filter(
                owner_id=data['_owner'], verified=True).latest('created_date')
            job_apply = JobApply.objects.create(
                field_id=data['_id'],
                search_params=search_params,
                candidate=candidate,
                user=verified_platform_cred
            )
            job_apply.save()

            logger.info("job apply data saved properly")

            return {"message": 'success saving job apply', "job_apply": job_apply}

        except Exception as e:
            logger.error(f"error saving job apply {str(e)}")
            return {"message": 'error saving job apply', "error": str(e)}
  ############## Apply jobs ##############
    def fastapiApplyJobs(self, jobapply: JobApply):
        try:
            # Create an instance of the FastAPIClient with the base URL of your FastAPI app
            fastapi_client = FastAPIClient()  # Replace with your FastAPI URL
            forward_request = {
                "user":
                {
                    "email": jobapply.user.email,
                    "password": jobapply.user.password,
                    "platform": jobapply.user.platform,
                    "owner": jobapply.user.owner_id,
                    "field_id": jobapply.user.field_id,
                    "created_date": jobapply.user.created_date
                },
                "search_params":
                {
                    "job": jobapply.search_params.job,
                    "location": jobapply.search_params.location,
                    "limit": str(jobapply.search_params.limit),
                },
                "candidate": {
                    "firstname": jobapply.candidate.firstname,
                    "lastname": jobapply.candidate.lastname,
                    "gender": jobapply.candidate.gender,
                    "resume": jobapply.candidate.resume,
                    "phone_number": jobapply.candidate.phone_number,
                    "address": {
                        "street": str(jobapply.candidate.address.street_name) +" "+ str(jobapply.candidate.address.street_number),
                        "city": jobapply.candidate.address.city,
                        "plz": str(jobapply.candidate.address.zip),
                        "country": jobapply.candidate.address.country,
                    },
                    "start_date": jobapply.candidate.start_date,
                    "limit": str(jobapply.candidate.limit),
                    "visa_required": jobapply.candidate.visa_required,
                    "years_experience": str(jobapply.candidate.years_experience),
                    "desired_salary": str(jobapply.candidate.desired_salary),
                    "experiences": [{"job_title": exp.job_title, "company": exp.company, "duration": exp.duration} for exp in Experience.objects.filter(candidate=jobapply.candidate)],
                    "educations": [{"university": edu.university, "degree": edu.degree, "duration": edu.duration} for edu in Education.objects.filter(candidate=jobapply.candidate)],
                    "skills": {
                        "Languages": {lang.name: lang.proficiency for lang in jobapply.candidate.skills.languages.all()},
                        "Softwares": {sw.name: sw.proficiency for sw in jobapply.candidate.skills.softwares.all()}
                    }
                },
                "field_id": jobapply.field_id  # added to retrieve field in jobsesrch collection
            }
            
            # Use the FastAPIClient to send the data to the FastAPI endpoint asynchronously
            response_data = fastapi_client.applyJobs(forward_request)
            logger.info("response: %s", response_data)
            wixClientCred = WixClient()
            if response_data["status"] == 'ok':  # success
                # save job count to data: add job count to jobApplication
                # data.save()  # Save the changes to the database
                #logger.info("response fast api: %s ", response_data)
                wixClientCred.putJobsApplyResp(response_data)
                return response_data
            else:
                logger.error(
                    f"error with login data {response_data['status_code']}")
                wixClientCred.putJobsApplyResp(response_data)
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
                target=self.fastapiApplyJobs, args=[database_response["job_apply"]])
            forward_thread.start()
            # Respond immediately
            return JsonResponse({'message': 'job apply started', "status": 202}, status=202)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in the request', "status": 400}, status=400)
