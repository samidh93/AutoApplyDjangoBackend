from django.urls import path
from .views import jobs_apply_view, jobs_search_view, platforms_view, applications_view, jobs_found_view, jobs_searched_view, jobs_applied_view

urlpatterns = [
    # verify cred platform 
    path('applications/platform/verify/', platforms_view.VerifyPlatformCredDataView.as_view(), name='verify_platform_cred'),
    # list all saved applications in db
    path('applications/',applications_view.ApplicationListView.as_view(), name='list_applications_requests'),
    # found jobs
    path('applications/jobs/found/', jobs_found_view.JobFoundDataView.as_view(), name='jobs_found'),
    # search jobs
    path('applications/jobs/search/', jobs_search_view.JobSearchDataView.as_view(), name='search_jobs'),
    path('applications/jobs/searched/', jobs_searched_view.JobSearchedDataView.as_view(), name='jobs_searched'),
    # apply jobs
    path('applications/jobs/apply/', jobs_apply_view.JobApplyDataView.as_view(), name='apply_jobs'),
    path('applications/jobs/applied/', jobs_applied_view.JobAppliedDataView.as_view(), name='jobs_applied'),
]
