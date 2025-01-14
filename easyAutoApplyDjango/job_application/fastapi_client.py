import requests
import json
import logging
logger = logging.getLogger(__name__)

class FastAPIClient:
    def __init__(self):
        self.PORT = "3991"
        self.IP = "127.0.0.1"  # paste fast api instance ip 172.31.32.169
        self.base_url =  f"http://{self.IP}:{self.PORT}"
        # JobApplyApi
        self.JobApplyApi_apply = f"{self.base_url}/api/job/apply/" # post apply jobs
        self.JobApplyApi_jobs_applied = f"{self.base_url}/api/job/apply/jobs_applied" # get applied jobs (success)
        # JobSearchApi
        self.JobSearchApi_search = f"{self.base_url}/api/job/search/" # post search jobs
        self.JobSearchApi_jobs_found= f"{self.base_url}/api/job/search/jobs_found" # get found jobs (stored)
        self.JobSearchApi_jobs_searched= f"{self.base_url}/api/job/search/jobs_searched" # get found jobs (stored)
        # LinkedinCredApi
        self.LinkedinCredApi_verify = f"{self.base_url}/api/platform/linkedin/verify/" # post search jobs
        self.LinkedinCredApi_cookies= f"{self.base_url}/api/platform/linkedin/cookies/" # get found jobs (stored)     

    #POST
    def verifyPlatformCred(self, item_data:dict):
        try:
            # Send the POST request to FastAPI
            response = requests.post(self.LinkedinCredApi_verify , json=item_data)
            # Check the response status code
            response_data = response.json()
            if response.status_code == 200:
                # Request was successful
                logger.info("response fast api server: %s", response_data)
                return {"message": "verified login", "data": response_data, "status_code": response.status_code}
            else:
                logger.error(f"error from fastapi server, {response_data}, response status code {response.status_code}")
                return {
                    "error": "Failed to login",
                    "data": {
                        "response_data": response_data,
                        "data": {
                            "_owner": item_data["user"]["owner"],
                            "_id": item_data["user"]["field_id"],
                            "verified": False
                        }
                    },
                    "status_code": response.status_code
                }
        except requests.exceptions.RequestException as e:
            logger.error(f"error with fastapi server {str(e)}")
            return {"error": "Error sending POST request", "exception": str(e)}
    # GET
    def getPlatformCredCookies(self, params):
        try:
            # Send the GET request to FastAPI
            response = requests.get(self.LinkedinCredApi_cookies , json=params)
            # Check the response status code
            if response.status_code == 200:
                # Request was successful
                response_data = response.json()
                logger.info("response fast api server: %s", response_data)
                return response_data
            else:
                return {"error": "Failed to get cookies", "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": "Error sending GET request", "exception": str(e)}
    
    #POST
    def searchJobs(self, item_data:dict):
        try:
            # Send the POST request to FastAPI
            logger.info(f"data sended: {item_data}")
            response = requests.post(self.JobSearchApi_search, json=item_data)
            logger.info("raw response fast api server: %s", response)

            # Check the response status code
            if response.status_code == 200:
                # Request was successful
                response_data = response.json()
                logger.info("response fast api server: %s", response_data)
                return response_data
            else:
                return {"error": "Failed to search jobs", "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": "Error sending POST request", "exception": str(e)}

    # GET
    def getJobsFoundAfterSearch(self, params):
        try:
            # Send the GET request to FastAPI
            response = requests.get(self.JobSearchApi_jobs_found , json=params)
            # Check the response status code
            if response.status_code == 200:
                # Request was successful
                response_data = response.json()
                logger.info("response fast api server: %s", response_data)
                return response_data
            else:
                return {"error": "Failed to get jobs search found", "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": "Error sending GET request", "exception": str(e)}

    # GET
    def getJobsSearchedAfterSearch(self, params):
        try:
            # Send the GET request to FastAPI
            response = requests.get(self.JobSearchApi_jobs_found , json=params)
            # Check the response status code
            if response.status_code == 200:
                # Request was successful
                response_data = response.json()
                logger.info("response fast api server: %s", response_data)
                return response_data
            else:
                return {"error": "Failed to get jobs search found", "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": "Error sending GET request", "exception": str(e)}   
    #POST
    def applyJobs(self, item_data:dict):
        try:
            # Serialize item_data to JSON
            #json_data = json.dumps(item_data)
            # Send the POST request to FastAPI
            logger.info(f"data sended: {item_data}")
            response = requests.post(self.JobApplyApi_apply, json=item_data)
            # Check the response status code
            if response.status_code == 200:
                # Request was successful
                response_data = response.json()
                logger.info("response fast api server: %s", response_data)
                return response_data
            else:
                return {"error": "Failed to apply jobs", "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": "Error sending POST request", "exception": str(e)}

   # GET
    def getJobsAppliedAfterApply(self, params):
        try:
            # Send the GET request to FastAPI
            response = requests.get(self.JobApplyApi_jobs_applied , json=params)
            # Check the response status code
            if response.status_code == 200:
                # Request was successful
                response_data = response.json()
                logger.info("response fast api server: %s", response_data)
                return response_data
            else:
                return {"error": "Failed to get jobs apply applied", "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": "Error sending GET request", "exception": str(e)}
        