import requests
import json
import logging
logger = logging.getLogger(__name__)

class WixClient:
    def __init__(self):
        self.base_url =  "https://www.easyapplyhub.com/_functions"
        # constrcut with the name of the function
        # LinkedinCredResp
        self.LinkedinCredResp = f"{self.base_url}/LinkedinCredResp" # resp platform cred verification
        self.JobsFoundCountResp = f"{self.base_url}/JobsFoundCountResp" # resp platform cred verification
        self.JobsSearchResp = f"{self.base_url}/JobsSearchResp" # resp platform cred verification
        self.JobsSearchedCountResp = f"{self.base_url}/JobsSearchedCountResp" # resp platform cred verification
        self.JobsApplyResp = f"{self.base_url}/JobsApplyResp" # resp platform cred verification
        self.JobsAppliedCountResp = f"{self.base_url}/JobsAppliedResp" # resp platform cred verification

    #PUT
    def putPlatformCredResp(self, request:dict):
        try:
            # Send the POST request to wix
            #request = json.dumps(request)
            #logger.info(f"passed request to wix: {request} with type {type(request)}")
            response = requests.put(self.LinkedinCredResp , json=request)
            # Check the response status code
            if response.status_code == 201:
                # Request was successful
                logger.info("response wix server: %s", response)
                return {"message": "verified login", "data": response.status_code, "status_code": response.status_code}
            else:
                logger.error(f"error from wix server, {response.status_code}")
                return {"error": "Failed to login", "data": response.status_code, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            logger.error(f"error with wix server {str(e)}")
            return {"error": "Error sending POST request", "exception": str(e)}

    #PUT
    def putJobsFoundCountResp(self, request:dict):
        try:
            # Send the POST request to wix
            #request = json.dumps(request)
            #logger.info(f"passed request to wix: {request} with type {type(request)}")
            response = requests.put(self.JobsFoundCountResp , json=request)
            # Check the response status code
            if response.status_code == 201:
                # Request was successful
                logger.info("response wix server: %s", response)
                return {"message": "search job count success",  "status_code": response.status_code}
            else:
                logger.error(f"error from wix server, {response.status_code}")
                return {"error": "Failed to search job count", "data": response.status_code, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            logger.error(f"error with wix server {str(e)}")
            return {"error": "Error sending POST request", "exception": str(e)}

   #PUT
    def putJobsSearchedCountResp(self, request:dict):
        try:
            # Send the POST request to wix
            #request = json.dumps(request)
            #logger.info(f"passed request to wix: {request} with type {type(request)}")
            response = requests.put(self.JobsSearchedCountResp , json=request)
            # Check the response status code
            if response.status_code == 201:
                # Request was successful
                logger.info("response wix server: %s", response)
                return {"message": "searched count job success",  "status_code": response.status_code}
            else:
                logger.error(f"error from wix server, {response.status_code}")
                return {"error": "Failed to collect searched count jobs", "data": response.status_code, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            logger.error(f"error with wix server {str(e)}")
            return {"error": "Error sending POST request", "exception": str(e)}
        
   #PUT
    def putJobsSearchResp(self, request:dict):
        try:
            # Send the POST request to wix
            #request = json.dumps(request)
            #logger.info(f"passed request to wix: {request} with type {type(request)}")
            response = requests.put(self.JobsSearchResp , json=request)
            # Check the response status code
            if response.status_code == 201:
                # Request was successful
                logger.info("response wix server: %s", response)
                return {"message": "search job success",  "status_code": response.status_code}
            else:
                logger.error(f"error from wix server, {response.status_code}")
                return {"error": "Failed to search jobs", "data": response.status_code, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            logger.error(f"error with wix server {str(e)}")
            return {"error": "Error sending POST request", "exception": str(e)}
        
   #PUT
    def putJobsApplyResp(self, request:dict):
        try:
            # Send the POST request to wix
            #request = json.dumps(request)
            #logger.info(f"passed request to wix: {request} with type {type(request)}")
            response = requests.put(self.JobsApplyResp , json=request)
            # Check the response status code
            if response.status_code == 201:
                # Request was successful
                logger.info("response wix server: %s", response)
                return {"message": "Apply job success",  "status_code": response.status_code}
            else:
                logger.error(f"error from wix server, {response.status_code}")
                return {"error": "Failed to apply jobs", "data": response.status_code, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            logger.error(f"error with wix server {str(e)}")
            return {"error": "Error sending POST request", "exception": str(e)}
        
   #PUT
    def putJobsAppliedCountResp(self, request:dict):
        try:
            # Send the POST request to wix
            #request = json.dumps(request)
            #logger.info(f"passed request to wix: {request} with type {type(request)}")
            response = requests.put(self.JobsAppliedCountResp , json=request)
            # Check the response status code
            if response.status_code == 201:
                # Request was successful
                logger.info("response wix server: %s", response)
                return {"message": "Applied job count success",  "status_code": response.status_code}
            else:
                logger.error(f"error from wix server, {response.status_code}")
                return {"error": "Failed to get applied jobs count", "data": response.status_code, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            logger.error(f"error with wix server {str(e)}")
            return {"error": "Error sending POST request", "exception": str(e)}