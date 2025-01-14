# models.py
from django.db import models
from django.utils import timezone

class jobPlatformCred(models.Model):
    owner_id = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_date = models.CharField(max_length=255)
    updated_date = models.CharField(max_length=255)
    field_id = models.CharField(max_length=255) # identify field id on frontend table
    verified = models.BooleanField(default=False)
    cookies = models.CharField(max_length=255)
    
class jobApplication(models.Model):
    owner_id = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    job_location = models.CharField(max_length=255)
    resume = models.URLField(max_length=255) 
    platform = models.CharField(max_length=255)
    created_date = models.CharField(max_length=255)
    updated_date = models.CharField(max_length=255)
    field_id = models.CharField(max_length=255) # identify field id on frontend table
    limit = models.IntegerField(null=True)
  # Create a ForeignKey relationship to jobPlatformCred using owner_id
    platform_cred = models.ForeignKey(jobPlatformCred, on_delete=models.CASCADE, null=True)

class SearchParams(models.Model):
    job = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    limit = models.IntegerField()    

class JobSearch(models.Model):
    user = models.ForeignKey(jobPlatformCred, on_delete=models.CASCADE)
    search_params = models.ForeignKey(SearchParams, on_delete=models.CASCADE)
    field_id = models.CharField(max_length=255) # identify field id on frontend table

class Address(models.Model):
    street_name = models.CharField(max_length=255)
    street_number = models.IntegerField()
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=10)
    country = models.CharField(max_length=255)

class Experience(models.Model):
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)

class Education(models.Model):
    degree = models.CharField(max_length=50)
    university = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)

class Language(models.Model):
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=20)

class Software(models.Model):
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=20)

class Skill(models.Model):
    languages = models.ManyToManyField(Language, related_name='skills')
    softwares = models.ManyToManyField(Software, related_name='skills')
    
class Candidate(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    resume = models.URLField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    limit = models.IntegerField()
    visa_required = models.CharField(max_length=10)
    years_experience = models.IntegerField()
    desired_salary = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    experiences = models.ManyToManyField(Experience)
    educations = models.ManyToManyField(Education)
    skills = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)

class JobApply(models.Model):
    field_id = models.CharField(max_length=255) # identify field id on frontend table
    user = models.ForeignKey(jobPlatformCred, on_delete=models.CASCADE)
    search_params = models.ForeignKey(SearchParams, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)


