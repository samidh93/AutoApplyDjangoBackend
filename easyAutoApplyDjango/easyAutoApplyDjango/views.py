from django.http import HttpResponse
from django.shortcuts import render

def root_view(request):
    return render(request, 'authentication/welcome.html')

