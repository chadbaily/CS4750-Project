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

users = ['ceb4aq_a', 'ceb4aq_b', 'ceb4aq_c', 'ceb4aq_d']
db_user = 'ceb4aq'


def home(request):
    global db_user
    print(db_user)
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response
    # Return the home page
    return render(request, 'home.block.html', {"login": user})


def actors(request):
    global db_user
    print(db_user)

    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response
    # Open database connection

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

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

    return render(request, 'actors.block.html', {"actors": actors, "login": user})


def edit_actors(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    if pk is None:
        return

    return render(request, 'edit-actor.block.html', {"login": user})


def update_actor(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response
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
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Update
            cursor.execute("UPDATE Actor SET FirstN = '" + first_name + "', MiddleN = '" + middle_name + "', LastN = '" +
                           last_name + "', Gender = '" + gender + "', DOB = '" + dob + "' WHERE ActorID = " + pk)
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('home'), {"login": user})
        else:
            print("form is false")
            return HttpResponseRedirect(reverse('edit_actor', args=[pk]), {"login": user})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Person()

    return HttpResponseRedirect(reverse('edit_actor', args=[pk]), {"login": user})


def create_actor(request):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    return render(request, 'create-actor.block.html', {"login": user})


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
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")

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
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response
    # Open database connection
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

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

    return render(request, 'crews.block.html', {"crews": crews, "login": user})


def edit_crews(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    if pk is None:
        return

    return render(request, 'edit-crew.block.html', {"login": user})


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
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")

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
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    return render(request, 'create-crew.block.html', {"login": user})


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
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")

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
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response
    # Open database connection
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

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

    return render(request, 'media.block.html', {"medias": medias, "login": user})


def info_media(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    if pk is None:
        return

    # ensure the pk is safe
        pk = escape(pk)

    # Get the information about the media

    # Open database connection
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the media
    cursor.execute("SELECT * FROM Media WHERE MediaID = " + pk)

    # Fetch all rows
    data = cursor.fetchall()

    if len(data) == 0 or len(data) > 1:
        return HttpResponseRedirect(reverse('home'))

    if len(data) == 1:
        print(data)
        row = data[0]
        media = {
            "pk": row[0],
            "media_name": str(row[1]) + " (" + str(row[2]) + ")",
            "mtype": row[3],
            "description": row[5]
        }

    # Get all the actors references
    actors_cursor = db.cursor()

    actors_cursor.execute("SELECT * FROM Actors WHERE MediaID = " + pk)

    # Fetch all rows
    actors_data = actors_cursor.fetchall()
    print(actors_data)
    actors = []
    for row in actors_data:
        # Get all the actors
        actor_cursor = db.cursor()
        actor_cursor.execute(
            "SELECT * FROM Actor WHERE ActorID = " + str(row[1]))
        # Fetch all rows
        actor_data = actor_cursor.fetchall()
        print(actor_data)
        for line in actor_data:
            actor = {
                "pk": line[0],
                "name": str(line[1]) + " " + str(line[3]),
                "role_name": str(row[2]),
                "gender": line[5]
            }
            actors.append(actor)

    crews_cursor = db.cursor()
    crews_cursor.execute("SELECT * FROM Crews WHERE MediaID = " + pk)

    # Fetch all rows
    crews_data = crews_cursor.fetchall()
    print(crews_data)
    crews = []
    for row in crews_data:
        # Get all the crews
        crew_cursor = db.cursor()
        crew_cursor.execute(
            "SELECT * FROM Crew WHERE CrewID = " + str(row[0]))
        # Fetch all rows
        crew_data = crew_cursor.fetchall()
        print(crew_data)
        for line in crew_data:
            crew = {
                "pk": line[0],
                "name": str(line[1]) + " " + str(line[3]),
                "ctype": str(row[2]),
            }
            crews.append(crew)

    memes_cursor = db.cursor()
    memes_cursor.execute("SELECT * FROM InReferenceTo WHERE MediaID = " + pk)

    # Fetch all rows
    memes_data = memes_cursor.fetchall()
    print(memes_data)
    memes = []
    for row in memes_data:
        # Get all the memes
        meme_cursor = db.cursor()
        meme_cursor.execute(
            "SELECT * FROM Memes WHERE MemeID = " + str(row[0]))
        # Fetch all rows
        meme_data = meme_cursor.fetchall()
        print(meme_data)
        for line in meme_data:
            meme = {
                "pk": line[0],
                "genre": str(line[1]),
                "format": str(line[2]),
                "description" : str(line[3])
            }
            memes.append(meme)






    # Get all the actors references
    reviews_cursos = db.cursor()

    reviews_cursos.execute("SELECT * FROM Review_On WHERE MediaID = " + pk)

    # Fetch all rows
    reviews_data = reviews_cursos.fetchall()
    print("Reviews on " + pk)
    print(reviews_data)
    reviews = []
    for row in reviews_data:
        # Get all the reviews
        review_cursor = db.cursor()
        review_cursor.execute(
            "SELECT * FROM Review WHERE ReviewID = " + str(row[0]))
        # Fetch all rows
        review_data = review_cursor.fetchall()
        print(review_data)
        for line in review_data:
            review = {
                "pk": line[0],
                "rating": str(line[2]),
                "description": str(line[3])
            }
            reviews.append(review)
    # disconnect from server
    db.close()
    return render(request, 'info-media.block.html', {"media": media, "actors": actors, "crews":crews, "memes":memes, "reviews": reviews, "login": user})


def edit_media(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    if pk is None:
        return

    return render(request, 'edit-media.block.html', {"login": user})


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
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")

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
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    return render(request, 'create-media.block.html', {"login": user})


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
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")
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
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response
    # Open database connection
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")
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

    return render(request, 'meme.block.html', {"memes": memes, "login": user})


def edit_meme(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    if pk is None:
        return

    return render(request, 'edit-meme.block.html', {"login": user})


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
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")
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
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    return render(request, 'create-meme.block.html', {"login": user})


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
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")
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


def submit_login(request):
    if request.method == 'POST':

        form = Login(request.POST)

        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']

            # Prepare to interact with the DB
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")

            cursor = db.cursor()

            # Get all the media
            cursor.execute("SELECT * FROM User_Login WHERE user_name = '" +
                           user_name+"' and password = '"+password+"'")

            # Fetch all rows
            data = cursor.fetchall()
            # disconnect from server
            db.close()
            print(data)
            if(len(data) == 1):
                priv = data[0][3]
                # Add cookie
                response = HttpResponseRedirect(reverse('media'))
                response.set_cookie("user", priv)

                global users

                db_user = users[priv]
                print("login: " + str(db_user))

                # Delete cookie
                # response = HttpResponseRedirect(reverse('login'))
                # response.delete_cookie("auth")
                # return response
                return response
            else:
                return HttpResponseRedirect(reverse('login'))


def login(request):
    return render(request, 'login.block.html')


def review(request):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response
    # Open database connection
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the meme
    cursor.execute("SELECT * FROM Review")

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    reviews = []
    for row in data:
        mediaCursor = db.cursor()
        mediaCursor.execute(
            "SELECT * FROM Media WHERE MediaID = " + str(row[1]))
        mediaData = mediaCursor.fetchall()
        # print(mediaData)
        review = {
            "pk": row[0],
            "media_name": str(mediaData[0][1]) + " (" + str(mediaData[0][2]) + ")",
            "rating": str(row[2]),
            "description": str(row[3])
        }
        reviews.append(review)

    # disconnect from server
    db.close()

    return render(request, 'review.block.html', {"reviews": reviews, "login": user})


def submit_review(request):
    if request.method == 'POST':

        form = Review(request.POST)

        if form.is_valid():

            media_id = form.cleaned_data['media_id']
            rating = form.cleaned_data['rating']
            description = form.cleaned_data['description']

            # Update the DB
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Insert
            cursor.execute("INSERT INTO Review (MediaID,Rating,Description) VALUES ('" +
                           media_id + "','" + rating + "','" + description + "')")
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('review'))


def update_review(request, pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Review(request.POST)
        # print(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # print(form.cleaned_data)
            media_id = form.cleaned_data['media_id']
            rating = form.cleaned_data['rating']
            description = form.cleaned_data['description']

            # ensure the pk is safe
            pk = escape(pk)

            # Update the DB
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Update
            cursor.execute("UPDATE Review SET MediaID = '" + media_id + "', Rating = '" + rating +
                           "', Description = '" + description + "' WHERE ReviewID = " + pk)

            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('review'))
        else:
            print("form is false")
            return HttpResponseRedirect(reverse('edit_review', args=[pk]))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Review()

    return HttpResponseRedirect(reverse('edit_review', args=[pk]))


def edit_review(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response
    if pk is None:
        return

    return render(request, 'edit-review.block.html', {"login": user})


def create_review(request):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response
    return render(request, 'create-review.block.html', {"login": user})


def info_actor(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response
    if pk is None:
        return

    # ensure the pk is safe
        pk = escape(pk)

    # Get the information about the media

    # Open database connection
    db = pymysql.connect("mysql.cs.virginia.edu", "ceb4aq", "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the media
    cursor.execute("SELECT * FROM Actor WHERE ActorID = " + pk)

    # Fetch all rows
    data = cursor.fetchall()

    if len(data) == 0 or len(data) > 1:
        return HttpResponseRedirect(reverse('home'))

    if len(data) == 1:
        print(data)
        row = data[0]
        actor = {
            "pk": row[0],
            "actor_name": str(row[1]) + " " + str(row[3]),
            "dob": row[4],
            "gender": row[5],
            "pob" : str(row[6]) + ", " + str(row[7])
        }

    # Get all the actors references
    actors_cursor = db.cursor()

    actors_cursor.execute("SELECT * FROM Actors WHERE ActorID = " + pk)

    # Fetch all rows
    actors_data = actors_cursor.fetchall()
    print(actors_data)
    medias = []
    for row in actors_data:
        # Get all the actors
        media_cursor = db.cursor()
        media_cursor.execute(
            "SELECT * FROM Media WHERE MediaID = " + str(row[0]))
        # Fetch all rows
        media_data = media_cursor.fetchall()
        print(media_data)
        for line in media_data:
            media = {
                "pk": line[0],
                "name": str(line[1]) + " (" + str(line[2]) + ")",
                "role_name": str(row[2]),
            }
            medias.append(media)

    # Get all the actors references

    # disconnect from server
    db.close()

    return render(request, 'info-actor.block.html', {"medias": medias, "actor": actor,"login":user})



def logout(request):
    response = HttpResponseRedirect(reverse('login'))
    response.delete_cookie("user")
    return response

def info_crew(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response
    if pk is None:
        return

    # ensure the pk is safe
        pk = escape(pk)

    # Get the information about the media

    # Open database connection
    db = pymysql.connect("mysql.cs.virginia.edu", "ceb4aq", "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the media
    cursor.execute("SELECT * FROM Crew WHERE CrewID = " + pk)

    # Fetch all rows
    data = cursor.fetchall()

    if len(data) == 0 or len(data) > 1:
        return HttpResponseRedirect(reverse('home'))

    if len(data) == 1:
        print(data)
        row = data[0]
        crew = {
            "pk": row[0],
            "crew_name": str(row[1]) + " " + str(row[3]),
            "dob": row[4],
            "ctype": row[5],
            
        }

    # Get all the crews references
    actors_cursor = db.cursor()

    actors_cursor.execute("SELECT * FROM Crews WHERE CrewID = " + pk)

    # Fetch all rows
    actors_data = actors_cursor.fetchall()
    print(actors_data)
    medias = []
    for row in actors_data:
        # Get all the crews
        media_cursor = db.cursor()
        media_cursor.execute(
            "SELECT * FROM Media WHERE MediaID = " + str(row[0]))
        # Fetch all rows
        media_data = media_cursor.fetchall()
        print(media_data)
        for line in media_data:
            media = {
                "pk": line[0],
                "name": str(line[1]) + " (" + str(line[2]) + ")",
                "ctype": str(row[2]),
            }
            medias.append(media)

    # Get all the crews references

    # disconnect from server
    db.close()

    return render(request, 'info-crew.block.html', {"medias": medias, "crew": crew,"login":user})

