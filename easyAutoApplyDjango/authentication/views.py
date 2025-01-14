# views.py

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from .forms import CustomUserCreationForm
import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import render

def root_view(request):
    return render(request, 'authentication/welcome.html')

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "authentication/registration.html"
    
    def form_valid(self, form):
        # Save the user and return a JSON response for success
        logger.info(self.request.body.decode())
        self.object = form.save()
        response_data = {'message': 'User registered successfully'}
        return JsonResponse(response_data, status=201)

    def form_invalid(self, form):
        # Handle form validation errors and return a JSON response for errors
        logger.info(self.request.body.decode())
        errors = form.errors
        return JsonResponse({'errors': errors}, status=400)

class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request): 
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return JsonResponse({'message': 'User logout successfully'}, status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return JsonResponse({'errors': 'error logging out'},status=status.HTTP_400_BAD_REQUEST)
          
