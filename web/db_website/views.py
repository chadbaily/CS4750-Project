from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
import json
import requests
import pymysql

# Create your views here.


def home(request):
      # Return the home page
    return render(request, 'home.block.html')


def test(request):
    # Open database connection
    db = pymysql.connect("database", "root", "example", "project")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print("Database version : %s " % data)

    # disconnect from server
    db.close()

    return HttpResponse("Database version : %s " % data)
