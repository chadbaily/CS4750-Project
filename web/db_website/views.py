from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
import json
import requests

# Create your views here.


def home(request):
      # Return the home page
    return render(request, 'home.block.html')
