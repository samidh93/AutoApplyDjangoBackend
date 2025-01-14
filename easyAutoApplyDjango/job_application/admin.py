from django.contrib import admin
from .models import *

class jobApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_id', 'job_title', 'job_location', 'resume', 'platform', 'created_date', 'updated_date', 'field_id')

class jobPlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_id', 'platform', 'email', 'password','created_date', 'updated_date', 'field_id', 'verified', 'cookies')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'street_name', 'street_number', 'city', 'zip', 'country')

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title', 'company', 'duration')

class EducationAdmin(admin.ModelAdmin):
    list_display = ('id', 'university', 'degree', 'duration')

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'proficiency')

class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'proficiency')

class SkillAdmin(admin.ModelAdmin):
    list_display = ('id',)  # No specific fields for Skill, you can adjust it as needed

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'gender', 'phone_number', 'start_date', 'address', 'limit', 'visa_required', 'years_experience', 'desired_salary', 'resume')

class JobApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'field_id', 'user', 'search_params', 'candidate')

class SearchParamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'location', 'limit')

class JobSearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'search_params', 'field_id')

# Register the models with their respective admin classes
admin.site.register(SearchParams, SearchParamsAdmin)
admin.site.register(JobSearch, JobSearchAdmin)
# Register the models with their respective admin classes
admin.site.register(Address, AddressAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Software, SoftwareAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(JobApply, JobApplyAdmin)
# Register the model with the custom admin class
admin.site.register(jobApplication, jobApplicationAdmin)
admin.site.register(jobPlatformCred, jobPlatformAdmin)