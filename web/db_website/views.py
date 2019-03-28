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


def actors(request):
    # Open database connection
    db = pymysql.connect("database", "root", "example", "project")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the actors
    cursor.execute("SELECT * FROM Actor")

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    actors = []
    for row in data:
        actor = {
            "name": str(row[1]) + " " + str(row[3]),
            "gender": row[5]
        }
        actors.append(actor)

    # disconnect from server
    db.close()

    return render(request, 'actors.block.html', {"actors": actors})
