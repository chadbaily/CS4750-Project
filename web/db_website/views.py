from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.html import escape
from .forms import *
import json
import requests
import pymysql


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
            "pk": row[0],
            "name": str(row[1]) + " " + str(row[3]),
            "gender": row[5]
        }
        actors.append(actor)

    # disconnect from server
    db.close()

    return render(request, 'actors.block.html', {"actors": actors})


def edit_actors(request, pk):

    if pk is None:
        return

    return render(request, 'edit-actor.block.html')


def update_actor(request, pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Person(request.POST)
        # print(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # print(form.cleaned_data)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            gender = form.cleaned_data['gender']
            dob = form.cleaned_data['dob']

            # ensure the pk is safe
            pk = escape(pk)

            # print("UPDATE Actor SET FirstN = '" + first_name + "', MiddleN = '" + middle_name + "', LastN = '" +
            #       last_name + "', Gender = '" + gender + "', DOB = '" + dob + "'  WHERE ActorID = " + pk)

            # Update the DB
            db = pymysql.connect("database", "root", "example", "project")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Update
            cursor.execute("UPDATE Actor SET FirstN = '" + first_name + "', MiddleN = '" + middle_name + "', LastN = '" +
                           last_name + "', Gender = '" + gender + "', DOB = '" + dob + "' WHERE ActorID = " + pk)
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('home'))
        else:
            print("form is false")
            return HttpResponseRedirect(reverse('edit_actor', args=[pk]))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Person()

    return HttpResponseRedirect(reverse('edit_actor', args=[pk]))


def create_actor(request):

    return render(request, 'create-actor.block.html')


def submit_create_actor(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Person(request.POST)
        # print(request.POST)
        # check whether it's valid:
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            gender = form.cleaned_data['gender']
            dob = form.cleaned_data['dob']

            # Update the DB
            db = pymysql.connect("database", "root", "example", "project")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Insert
            cursor.execute("INSERT INTO Actor (FirstN, MiddleN, LastN, DOB, Gender) VALUES ('" +
                           first_name + "','" + middle_name + "','" + last_name + "','" + dob + "','" + gender + "')")
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('actors'))
        else:
            # print("form is false")
            return HttpResponseRedirect(reverse('create_actor'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Person()

    return HttpResponseRedirect(reverse('create_actor'))


def crews(request):
    # Open database connection
    db = pymysql.connect("database", "root", "example", "project")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the Crews
    cursor.execute("SELECT * FROM Crew")

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    crews = []
    for row in data:
        crew = {
            "pk": row[0],
            "name": str(row[1]) + " " + str(row[3]),
            "ctype": row[5]
        }
        crews.append(crew)

    # disconnect from server
    db.close()

    return render(request, 'crews.block.html', {"crews": crews})


def edit_crews(request, pk):

    if pk is None:
        return

    return render(request, 'edit-crew.block.html')


def update_crew(request, pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Crew(request.POST)
        # print(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # print(form.cleaned_data)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            ctype = form.cleaned_data['ctype']
            dob = form.cleaned_data['dob']

            # ensure the pk is safe
            pk = escape(pk)

            # print("UPDATE crew SET FirstN = '" + first_name + "', MiddleN = '" + middle_name + "', LastN = '" +
            #       last_name + "', Gender = '" + gender + "', DOB = '" + dob + "'  WHERE crewID = " + pk)

            # Update the DB
            db = pymysql.connect("database", "root", "example", "project")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Update
            cursor.execute("UPDATE Crew SET FirstN = '" + first_name + "', MiddleN = '" + middle_name + "', LastN = '" +
                           last_name + "', Type = '" + ctype + "', DOB = '" + dob + "' WHERE CrewID = " + pk)
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('home'))
        else:
            print("form is false")
            return HttpResponseRedirect(reverse('edit_crew', args=[pk]))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Crew()

    return HttpResponseRedirect(reverse('edit_crew', args=[pk]))


def create_crew(request):

    return render(request, 'create-crew.block.html')


def submit_create_crew(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Crew(request.POST)
        # print(request.POST)
        # check whether it's valid:
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            ctype = form.cleaned_data['ctype']
            dob = form.cleaned_data['dob']

            # Update the DB
            db = pymysql.connect("database", "root", "example", "project")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Insert
            cursor.execute("INSERT INTO Crew (FirstN, MiddleN, LastN, DOB, Type) VALUES ('" +
                           first_name + "','" + middle_name + "','" + last_name + "','" + dob + "','" + ctype + "')")
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('crews'))
        else:
            # print("form is false")
            return HttpResponseRedirect(reverse('create_crew'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Crew()

    return HttpResponseRedirect(reverse('create_crew'))


def media(request):
    # Open database connection
    db = pymysql.connect("database", "root", "example", "project")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the media
    cursor.execute("SELECT * FROM Media")

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    medias = []
    for row in data:
        media = {
            "pk": row[0],
            "media_name": str(row[1]) + " (" + str(row[2]) + ")",
            "mtype": row[3],
            "description": row[5]
        }
        medias.append(media)

    # disconnect from server
    db.close()

    return render(request, 'media.block.html', {"medias": medias})


def edit_media(request, pk):

    if pk is None:
        return

    return render(request, 'edit-media.block.html')


def update_media(request, pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Media(request.POST)
        # print(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # print(form.cleaned_data)
            media_name = form.cleaned_data["media_name"]
            year = form.cleaned_data['year']
            mtype = form.cleaned_data['mtype']
            genre = form.cleaned_data['genre']
            description = form.cleaned_data['description']
            mpaa_rating = form.cleaned_data['mpaa_rating']
            crit_rating = form.cleaned_data['crit_rating']

            # ensure the pk is safe
            pk = escape(pk)

            # print("UPDATE Media SET FirstN = '" + first_name + "', MiddleN = '" + middle_name + "', LastN = '" +
            #       last_name + "', Gender = '" + gender + "', DOB = '" + dob + "'  WHERE MediaID = " + pk)

            # Update the DB
            db = pymysql.connect("database", "root", "example", "project")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Update
            cursor.execute("UPDATE Media SET MediaName = '" + media_name + "', Year = '" + year +
                           "',Type = '" + mtype + "',Genre ='"+genre+"',Description = '"+description+"',MPAA_Rating = '" +
                           mpaa_rating+"',Crit_Rating = '"+crit_rating+"'WHERE MediaID = " + pk)

            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('media'))
        else:
            print("form is false")
            return HttpResponseRedirect(reverse('edit_media', args=[pk]))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Media()

    return HttpResponseRedirect(reverse('edit_media', args=[pk]))


def create_media(request):

    return render(request, 'create-media.block.html')


def submit_create_media(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Media(request.POST)
        # print(request.POST)
        # check whether it's valid:
        if form.is_valid():
            media_name = form.cleaned_data["media_name"]
            year = form.cleaned_data['year']
            mtype = form.cleaned_data['mtype']
            genre = form.cleaned_data['genre']
            description = form.cleaned_data['description']
            mpaa_rating = form.cleaned_data['mpaa_rating']
            crit_rating = form.cleaned_data['crit_rating']

            # Update the DB
            db = pymysql.connect("database", "root", "example", "project")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Insert
            cursor.execute("INSERT INTO Media (MediaName,Year,Type,Genre,Description,MPAA_Rating,Crit_Rating) VALUES ('" +
                           media_name + "','" + year + "','" + mtype + "','" + genre + "','" + description + "','" + mpaa_rating + "','" + crit_rating + "')")
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('media'))
        else:
            # print("form is false")
            return HttpResponseRedirect(reverse('create_media'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Media()

    return HttpResponseRedirect(reverse('create_media'))


def meme(request):
        # Open database connection
    db = pymysql.connect("database", "root", "example", "project")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the meme
    cursor.execute("SELECT * FROM Memes")

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    memes = []
    for row in data:
        meme = {
            "pk": row[0],
            "genre": str(row[1]),
            "format": str(row[2]),
            "description": str(row[3])
        }
        memes.append(meme)

    # disconnect from server
    db.close()

    return render(request, 'meme.block.html', {"memes": memes})


def edit_meme(request, pk):

    if pk is None:
        return

    return render(request, 'edit-meme.block.html')


def update_meme(request, pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Meme(request.POST)
        # print(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # print(form.cleaned_data)
            genre = form.cleaned_data['genre']
            description = form.cleaned_data['description']
            meme_format = form.cleaned_data['meme_format']

            # ensure the pk is safe
            pk = escape(pk)

            # Update the DB
            db = pymysql.connect("database", "root", "example", "project")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Update
            cursor.execute("UPDATE Memes SET Genre = '" + genre + "', Format = '" + meme_format +
                           "', Description = '" + description + "' WHERE MemeID = " + pk)

            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('meme'))
        else:
            print("form is false")
            return HttpResponseRedirect(reverse('edit_meme', args=[pk]))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Meme()

    return HttpResponseRedirect(reverse('edit_meme', args=[pk]))


def create_meme(request):

    return render(request, 'create-meme.block.html')


def submit_create_meme(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Meme(request.POST)
        # print(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # print(form.cleaned_data)
            genre = form.cleaned_data['genre']
            description = form.cleaned_data['description']
            meme_format = form.cleaned_data['meme_format']

            # Update the DB
            db = pymysql.connect("database", "root", "example", "project")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Insert
            cursor.execute("INSERT INTO Memes (Genre,Format,Description) VALUES ('" +
                           genre + "','" + description + "','" + meme_format + "')")
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('meme'))
        else:
            # print("form is false")
            return HttpResponseRedirect(reverse('create_meme'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Person()

    return HttpResponseRedirect(reverse('create_meme'))
