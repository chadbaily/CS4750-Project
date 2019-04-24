from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.html import escape
from django.contrib import messages
from .forms import *
import json
import csv
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
    try:
        cursor.execute("SELECT * FROM Actor")
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

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
        return HttpResponseRedirect(reverse('home'))

    pk = escape(pk)

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the actors
    try:
        cursor.execute("SELECT * FROM Actor WHERE ActorID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))
    except pymysql.err.InternalError as e:
        print("caught an error")
        messages.warning(request, "Error")
        return HttpResponseRedirect(reverse('edit_actor', args=[pk]))
    except pymysql.err.ProgrammingError as e:
        print("problem")
        messages.info(request, "Bad form data")
        return HttpResponseRedirect(reverse('edit_actor', args=[pk]))

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    row = data[0]
    actor = {
        "pk": row[0],
        "first_name": str(row[1]),
        "middle_name": str(row[2]),
        "last_name": str(row[3]),
        "DOB": str(row[4]),
        "gender": str(row[5]),
        "birth_country": str(row[6]),
        "birth_city": str(row[7]),
    }

    # disconnect from server
    db.close()

    return render(request, 'edit-actor.block.html', {"login": user, "actor": actor})


def delete_actor(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    pk = escape(pk)

    # Update the DB
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Update
    try:
        cursor.execute("DELETE FROM Actor WHERE ActorID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))
        # Save the changes
    db.commit()

    # disconnect from server
    db.close()

    return HttpResponseRedirect(reverse('actors'))


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
            birth_country = form.cleaned_data['birth_country']
            birth_city = form.cleaned_data['birth_city']

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
            try:
                cursor.execute("UPDATE Actor SET FirstN = '" + first_name + "', MiddleN = '" + middle_name + "', LastN = '" +
                               last_name + "', Gender = '" + gender + "', DOB = '" + dob + "', BirthCountry = '" + birth_country + "', BirthCity = '" + birth_city + "' WHERE ActorID = " + pk)
            except pymysql.err.OperationalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))
            except pymysql.err as e:
                print("problem")
                messages.info(request, "Bad form data")
                return HttpResponseRedirect(reverse('edit_actor', args=[pk]))
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('actors'), {"login": user})
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
        # check whether it's valid:
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            gender = form.cleaned_data['gender']
            dob = form.cleaned_data['dob']
            birth_country = form.cleaned_data['birth_country']
            birth_city = form.cleaned_data['birth_city']

            # Update the DB
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Insert
            try:
                cursor.execute("INSERT INTO Actor (FirstN, MiddleN, LastN, DOB, Gender, BirthCountry, BirthCity) VALUES ('" +
                               first_name + "','" + middle_name + "','" + last_name + "','" + dob + "','" + gender + "','" + birth_country + "','" + birth_city + "')")
            except pymysql.err.OperationalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))
            except pymysql.err as e:
                print("problem")
                messages.info(request, "Bad form data")
                return HttpResponseRedirect(reverse('create_actor'))
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('actors'))
        else:
            # print("form is false")
            messages.info(request, "Bad form data")
            return HttpResponseRedirect(reverse('create_actor'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Person()
        messages.info(request, "Bad form data")
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
    try:
        cursor.execute("SELECT * FROM Crew")
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

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
    pk = escape(pk)

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the actors
    try:
        cursor.execute("SELECT * FROM Crew WHERE CrewID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    row = data[0]
    crew = {
        "pk": row[0],
        "first_name": str(row[1]),
        "middle_name": str(row[2]),
        "last_name": str(row[3]),
        "dob": str(row[4]),
        "type": str(row[5]),
    }

    # disconnect from server
    db.close()

    return render(request, 'edit-crew.block.html', {"login": user, "crew": crew})


def delete_crew(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    pk = escape(pk)

    # Update the DB
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Update
    try:
        cursor.execute("DELETE FROM Crew WHERE CrewID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))
    except pymysql.err.InternalError as e:
        print("caught an error")
        messages.warning(request, "Error")
        return HttpResponseRedirect(reverse('edit_crew', args=[pk]))
    except pymysql.err.ProgrammingError as e:
        print("problem")
        messages.info(request, "Bad form data")
        return HttpResponseRedirect(reverse('edit_crew', args=[pk]))
        # Save the changes
    db.commit()

    # disconnect from server
    db.close()

    return HttpResponseRedirect(reverse('crews'))


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
            try:
                cursor.execute("UPDATE Crew SET FirstN = '" + first_name + "', MiddleN = '" + middle_name + "', LastN = '" +
                               last_name + "', Type = '" + ctype + "', DOB = '" + dob + "' WHERE CrewID = " + pk)
            except pymysql.err.OperationalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))
            except pymysql.err.InternalError as e:
                print("caught an error")
                messages.warning(request, "Error")
                return HttpResponseRedirect(reverse('edit_crew', args=[pk]))
            except pymysql.err.ProgrammingError as e:
                print("problem")
                messages.info(request, "Bad form data")
                return HttpResponseRedirect(reverse('edit_crew', args=[pk]))

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
            try:
                cursor.execute("INSERT INTO Crew (FirstN, MiddleN, LastN, DOB, Type) VALUES ('" +
                               first_name + "','" + middle_name + "','" + last_name + "','" + dob + "','" + ctype + "')")
            except pymysql.err.OperationalError or pymysql.err.ProgrammingError or pymysql.err.InternalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))
            except pymysql.err.InternalError as e:
                print("caught an error")
                messages.warning(request, "Please enter a valid birthdate")
                return HttpResponseRedirect(reverse('create_crew'))
            except pymysql.err.ProgrammingError as e:
                messages.info(request, "Bad form data")
                return HttpResponseRedirect(reverse('create_crew'))
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('crews'))
        else:
            # print("form is false")
            messages.info(request, "Bad form data")
            return HttpResponseRedirect(reverse('create_crew'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Crew()
    messages.info(request, "Bad form data")
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
    try:
        cursor.execute("SELECT * FROM Media")

    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

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
    try:
        cursor.execute("SELECT * FROM Media WHERE MediaID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

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
            "genre": row[4],
            "description": row[5],
            "rating": row[6]
        }

    # Get all the actors references
    actors_cursor = db.cursor()

    try:
        actors_cursor.execute("SELECT * FROM Actors WHERE MediaID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    # Fetch all rows
    actors_data = actors_cursor.fetchall()
    print(actors_data)
    actors = []
    for row in actors_data:
        # Get all the actors
        actor_cursor = db.cursor()
        try:
            actor_cursor.execute(
                "SELECT * FROM Actor WHERE ActorID = " + str(row[1]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))
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
    try:
        crews_cursor.execute("SELECT * FROM Crews WHERE MediaID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    # Fetch all rows
    crews_data = crews_cursor.fetchall()
    print(crews_data)
    crews = []
    for row in crews_data:
        # Get all the crews
        crew_cursor = db.cursor()

        try:
            crew_cursor.execute(
                "SELECT * FROM Crew WHERE CrewID = " + str(row[0]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))

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

    try:
        memes_cursor.execute(
            "SELECT * FROM InReferenceTo WHERE MediaID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    # Fetch all rows
    memes_data = memes_cursor.fetchall()
    print(memes_data)
    memes = []
    for row in memes_data:
        # Get all the memes
        meme_cursor = db.cursor()

        try:
            meme_cursor.execute(
                "SELECT * FROM Memes WHERE MemeID = " + str(row[0]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))
        # Fetch all rows
        meme_data = meme_cursor.fetchall()
        print(meme_data)
        for line in meme_data:
            meme = {
                "pk": line[0],
                "genre": str(line[1]),
                "format": str(line[2]),
                "description": str(line[3])
            }
            memes.append(meme)

    ref1_cursor = db.cursor()
    try:
        ref1_cursor.execute("SELECT * FROM Refers WHERE ReferencerID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    data = ref1_cursor.fetchall()
    print(data)
    references = []
    for row in data:
        m11_cursor = db.cursor()
        try:
            m11_cursor.execute(
                "SELECT * FROM Media WHERE MediaID = " + str(row[1]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))

        m11data = m11_cursor.fetchall()

        m12_cursor = db.cursor()
        try:
            m12_cursor.execute(
                "SELECT * FROM Media WHERE MediaID = " + str(row[2]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))
        m12data = m12_cursor.fetchall()
        ref1 = {
            "pk": row[0],
            "m1pk": m11data[0][0],
            "m1name": str(m11data[0][1]),
            "m2pk": m12data[0][0],
            "m2name": str(m12data[0][1]),
            "description": row[3]
        }
        references.append(ref1)

    ref2_cursor = db.cursor()
    try:
        ref2_cursor.execute("SELECT * FROM Refers WHERE ReferenceeID = "+pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    data = ref2_cursor.fetchall()
    print(data)
    referenced = []
    for row in data:
        m21_cursor = db.cursor()
        try:
            m21_cursor.execute(
                "SELECT * FROM Media WHERE MediaID = " + str(row[1]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))
        m21data = m21_cursor.fetchall()

        m22_cursor = db.cursor()
        try:
            m22_cursor.execute(
                "SELECT * FROM Media WHERE MediaID = " + str(row[2]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))
        m22data = m22_cursor.fetchall()
        ref2 = {
            "pk": row[0],
            "m1pk": m21data[0][0],
            "m1name": str(m21data[0][1]),
            "m2pk": m22data[0][0],
            "m2name": str(m22data[0][1]),
            "description": row[3]
        }
        referenced.append(ref2)

    # Get all the actors references
    reviews_cursos = db.cursor()

    try:
        reviews_cursos.execute("SELECT * FROM Review_On WHERE MediaID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    # Fetch all rows
    reviews_data = reviews_cursos.fetchall()
    print("Reviews on " + pk)
    print(reviews_data)
    reviews = []
    for row in reviews_data:
        # Get all the reviews
        review_cursor = db.cursor()
        try:
            review_cursor.execute(
                "SELECT * FROM Review WHERE ReviewID = " + str(row[0]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))
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
    return render(request, 'info-media.block.html', {"media": media, "actors": actors, "crews": crews, "memes": memes, "references": references, "referenced": referenced, "reviews": reviews, "login": user})


def edit_media(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    if pk is None:
        return

    pk = escape(pk)

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the actors
    try:
        cursor.execute("SELECT * FROM Media WHERE MediaID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    row = data[0]
    media = {
        "pk": row[0],
        "media_name": str(row[1]),
        "year": str(row[2]),
        "mtype": str(row[3]),
        "genre": str(row[4]),
        "description": str(row[5]),
        "rating": str(row[6]),
        "critic_rating": str(row[7])
    }

    # disconnect from server
    db.close()

    return render(request, 'edit-media.block.html', {"login": user, "media": media})


def delete_media(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    pk = escape(pk)

    # Update the DB
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Update
    try:
        cursor.execute("DELETE FROM Media WHERE MediaID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))
        # Save the changes
    db.commit()

    # disconnect from server
    db.close()

    return HttpResponseRedirect(reverse('media'))


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
            try:
                cursor.execute("UPDATE Media SET MediaName = '" + media_name + "', Year = '" + year +
                               "',Type = '" + mtype + "',Genre ='"+genre+"',Description = '"+description+"',MPAA_Rating = '" +
                               mpaa_rating+"',Crit_Rating = '"+crit_rating+"'WHERE MediaID = " + pk)
            except pymysql.err.OperationalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))
            except pymysql.err.ProgrammingError as e:
                print("problem")
                messages.info(request, "Bad form data")
                return HttpResponseRedirect(reverse('edit_media', args=[pk]))

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
            try:
                cursor.execute("INSERT INTO Media (MediaName,Year,Type,Genre,Description,MPAA_Rating,Crit_Rating) VALUES ('" +
                               media_name + "','" + year + "','" + mtype + "','" + genre + "','" + description + "','" + mpaa_rating + "','" + crit_rating + "')")
            except pymysql.err.OperationalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))
            except pymysql.err.ProgrammingError as e:
                messages.info(request, "Bad form data")
                return HttpResponseRedirect(reverse('create_media'))
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('media'))
        else:
            # print("form is false")
            messages.info(request, "Bad form data")
            return HttpResponseRedirect(reverse('create_media'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Media()
    messages.info(request, "Bad form data")
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
    try:
        cursor.execute("SELECT * FROM Memes")
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

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

    pk = escape(pk)

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the actors
    try:
        cursor.execute("SELECT * FROM Memes WHERE  MemeID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))
    except pymysql.err.InternalError as e:
        print("caught an error")
        messages.warning(request, "Error")
        return HttpResponseRedirect(reverse('edit_meme', args=[pk]))
    except pymysql.err.ProgrammingError as e:
        print("problem")
        messages.info(request, "Bad form data")
        return HttpResponseRedirect(reverse('edit_meme', args=[pk]))

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    row = data[0]
    meme = {
        "pk": row[0],
        "genre": str(row[1]),
        "format": str(row[2]),
        "description": str(row[3])
    }

    # disconnect from server
    db.close()

    return render(request, 'edit-meme.block.html', {"login": user, "meme": meme})


def delete_meme(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    pk = escape(pk)

    # Update the DB
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Update
    try:
        cursor.execute("DELETE FROM Memes WHERE MemeID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))
        # Save the changes
    db.commit()

    # disconnect from server
    db.close()

    return HttpResponseRedirect(reverse('meme'))


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
            try:
                cursor.execute("UPDATE Memes SET Genre = '" + genre + "', Format = '" + meme_format +
                               "', Description = '" + description + "' WHERE MemeID = " + pk)
            except pymysql.err.OperationalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))
            except pymysql.err.InternalError as e:
                print("caught an error")
                messages.warning(request, "Error")
                return HttpResponseRedirect(reverse('edit_meme', args=[pk]))
            except pymysql.err.ProgrammingError as e:
                print("problem")
                messages.info(request, "Bad form data")
                return HttpResponseRedirect(reverse('edit_meme', args=[pk]))

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
            try:
                cursor.execute("INSERT INTO Memes (Genre,Format,Description) VALUES ('" +
                               genre + "','" + description + "','" + meme_format + "')")
            except pymysql.err.OperationalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))
            except pymysql.err.ProgrammingError as e:
                messages.info(request, "Bad form data")
                return HttpResponseRedirect(reverse('create_meme'))
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('meme'))
        else:
            # print("form is false")
            messages.info(request, "Bad form data")
            return HttpResponseRedirect(reverse('create_meme'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Person()
    messages.info(request, "Bad form data")
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
            try:
                cursor.execute("SELECT * FROM User_Login WHERE user_name = '" +
                               user_name+"' and password = '"+password+"'")
            except pymysql.err.OperationalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))

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

    messages.warning(request, "Wrong username or password")
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
    try:
        cursor.execute("SELECT * FROM Review")
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    reviews = []
    for row in data:
        mediaCursor = db.cursor()
        try:
            mediaCursor.execute(
                "SELECT * FROM Media WHERE MediaID = " + str(row[1]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))
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
            try:
                cursor.execute("INSERT INTO Review (MediaID,Rating,Description) VALUES ('" +
                               media_id + "','" + rating + "','" + description + "')")
            except pymysql.err.OperationalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))
            except pymysql.err.ProgrammingError as e:
                messages.info(request, "Bad form data")
                return HttpResponseRedirect(reverse('create_review'))
            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('review'))
    messages.info(request, "Bad form data")
    return HttpResponseRedirect(reverse('create_review'))


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

            # Updatetry:
            try:
                cursor.execute("UPDATE Review SET MediaID = '" + media_id + "', Rating = '" + rating +
                               "', Description = '" + description + "' WHERE ReviewID = " + pk)
            except pymysql.err.OperationalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))
            except pymysql.err.InternalError as e:
                print("caught an error")
                messages.warning(request, "Error")
                return HttpResponseRedirect(reverse('edit_review', args=[pk]))
            except pymysql.err.ProgrammingError as e:
                print("problem")
                messages.info(request, "Bad form data")
                return HttpResponseRedirect(reverse('edit_review', args=[pk]))

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
        return HttpResponseRedirect(reverse('home'))

    pk = escape(pk)

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the actors
    try:
        cursor.execute("SELECT * FROM Review WHERE ReviewID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))
    except pymysql.err.InternalError as e:
        print("caught an error")
        messages.warning(request, "Error")
        return HttpResponseRedirect(reverse('edit_review', args=[pk]))
    except pymysql.err.ProgrammingError as e:
        print("problem")
        messages.info(request, "Bad form data")
        return HttpResponseRedirect(reverse('edit_review', args=[pk]))

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    row = data[0]
    review = {
        "pk": row[0],
        "mediaID": str(row[1]),
        "rating": str(row[2]),
        "description": str(row[3])
    }

    # disconnect from server
    db.close()

    return render(request, 'edit-review.block.html', {"login": user, "review": review})


def delete_review(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    pk = escape(pk)

    # Update the DB
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Update
    try:
        cursor.execute("DELETE FROM Review WHERE ReviewID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))
        # Save the changes
    db.commit()

    # disconnect from server
    db.close()

    return HttpResponseRedirect(reverse('review'))


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
    db = pymysql.connect("mysql.cs.virginia.edu",
                         "ceb4aq", "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the media
    try:
        cursor.execute("SELECT * FROM Actor WHERE ActorID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

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
            "pob": str(row[6]) + ", " + str(row[7])
        }

    # Get all the actors references
    actors_cursor = db.cursor()

    try:
        actors_cursor.execute("SELECT * FROM Actors WHERE ActorID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    # Fetch all rows
    actors_data = actors_cursor.fetchall()
    print(actors_data)
    medias = []
    for row in actors_data:
        # Get all the actors
        media_cursor = db.cursor()
        try:
            media_cursor.execute(
                "SELECT * FROM Media WHERE MediaID = " + str(row[0]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))
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

    return render(request, 'info-actor.block.html', {"medias": medias, "actor": actor, "login": user})


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
    db = pymysql.connect("mysql.cs.virginia.edu",
                         "ceb4aq", "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the media
    try:
        cursor.execute("SELECT * FROM Crew WHERE CrewID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

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

    try:
        actors_cursor.execute("SELECT * FROM Crews WHERE CrewID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    # Fetch all rows
    actors_data = actors_cursor.fetchall()
    print(actors_data)
    medias = []
    for row in actors_data:
        # Get all the crews
        media_cursor = db.cursor()
        try:
            media_cursor.execute(
                "SELECT * FROM Media WHERE MediaID = " + str(row[0]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))
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

    return render(request, 'info-crew.block.html', {"medias": medias, "crew": crew, "login": user})


def error(request):
    return render(request, 'error.block.html')


def refs(request):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response
    # Open database connection
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    ref_cursor = db.cursor()
    try:
        ref_cursor.execute("SELECT * FROM Refers")
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    data = ref_cursor.fetchall()
    print(data)
    refs = []
    for row in data:
        m1_cursor = db.cursor()
        try:
            m1_cursor.execute(
                "SELECT * FROM Media WHERE MediaID = " + str(row[1]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))
        m1data = m1_cursor.fetchall()

        m2_cursor = db.cursor()
        try:
            m2_cursor.execute(
                "SELECT * FROM Media WHERE MediaID = " + str(row[2]))
        except pymysql.err.OperationalError as e:
            print("caught an error")
            messages.error(request, "Permisson denied")
            return HttpResponseRedirect(reverse('error'))
        m2data = m2_cursor.fetchall()
        ref = {
            "pk": row[0],
            "m1pk": m1data[0][0],
            "m1name": str(m1data[0][1]),
            "m2pk": m2data[0][0],
            "m2name": str(m2data[0][1]),
            "description": row[3]
        }
        refs.append(ref)
    db.close()
    return render(request, "refs.block.html", {"references": refs, "login": user})


def create_reference(request):
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
    try:
        cursor.execute("SELECT * FROM Media")
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))
    except pymysql.err.ProgrammingError as e:
        messages.info(request, "Bad form data")
        return HttpResponseRedirect(reverse('create_actor'))

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    media = []
    for row in data:
        data = {
            "pk": str(row[0]),
            "media_name": str(row[1]) + "(" + str(row[2]) + ")"
        }
        media.append(data)

    return render(request, 'create-reference.block.html', {"login": user, "media": media})


def submit_create_reference(request):
    if request.method == 'POST':

        form = Reference(request.POST)

        if form.is_valid():

            referencer = form.cleaned_data['referencer']
            referencee = form.cleaned_data['referencee']
            location = form.cleaned_data['location']
            description = form.cleaned_data['description']

            # Update the DB
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Insert
            try:
                cursor.execute("INSERT INTO Refers (ReferencerID,ReferenceeID,Location,Description) VALUES ('" +
                               referencer + "','" + referencee + "','" + location + "','" + description + "')")
            except pymysql.err.OperationalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))
            except pymysql.err.ProgrammingError as e:
                messages.info(request, "Bad form data")
                return HttpResponseRedirect(reverse('create_reference'))

            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('references'))
            # print("form is false")
    messages.info(request, "Bad form data")
    return HttpResponseRedirect(reverse('create_reference'))


def edit_reference(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    if pk is None:
        return

    # ensure the pk is safe
    pk = escape(pk)

    # Open database connection
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Get all the meme
    try:
        cursor.execute("SELECT * FROM Media")
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    # Fetch all rows
    data = cursor.fetchall()
    print(data)
    media = []
    for row in data:
        data = {
            "pk": str(row[0]),
            "media_name": str(row[1]) + "(" + str(row[2]) + ")"
        }
        media.append(data)

    # Prepare to interact with the DB
    ref_cursor = db.cursor()

    # Get all the meme
    try:
        ref_cursor.execute("SELECT * FROM Refers WHERE ReferenceID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))

    data = ref_cursor.fetchall()

    row = data[0]
    reference = {
        "pk": str(row[0]),
        "referencerID": str(row[1]),
        "referenceeID": str(row[2]),
        "location": str(row[3]),
        "description": str(row[4])
    }

    return render(request, 'edit-reference.block.html', {"login": user, "media": media, "reference": reference})


def update_reference(request, pk):
    if request.method == 'POST':

        form = Reference(request.POST)
        if form.is_valid():

            referencer = form.cleaned_data['referencer']
            referencee = form.cleaned_data['referencee']
            location = form.cleaned_data['location']
            description = form.cleaned_data['description']

            pk = escape(pk)

            # Update the DB
            global db_user

            db = pymysql.connect("mysql.cs.virginia.edu",
                                 db_user, "ib5pW8ZR", "ceb4aq")

            # Prepare to interact with the DB
            cursor = db.cursor()

            # Insert
            try:
                cursor.execute("UPDATE Refers SET ReferencerID = '" +
                               referencer + "', ReferenceeID = '" + referencee + "', Location = '" + location + "', Description = '" + description + "' WHERE ReferenceID = " + pk)
            except pymysql.err.OperationalError as e:
                print("caught an error")
                messages.error(request, "Permisson denied")
                return HttpResponseRedirect(reverse('error'))
            except pymysql.err.ProgrammingError as e:
                messages.info(request, "Bad form data")
                return HttpResponseRedirect(reverse('edit_reference', args=[pk]))

            # Save the changes
            db.commit()

            # disconnect from server
            db.close()

            return HttpResponseRedirect(reverse('references'))
            # print("form is false")
    messages.info(request, "Bad form data")
    return HttpResponseRedirect(reverse('edit_reference', args=[pk]))


def delete_reference(request, pk):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    pk = escape(pk)

    # Update the DB
    global db_user

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    # Prepare to interact with the DB
    cursor = db.cursor()

    # Update
    try:
        cursor.execute("DELETE FROM Refers WHERE ReferenceID = " + pk)
    except pymysql.err.OperationalError as e:
        print("caught an error")
        messages.error(request, "Permisson denied")
        return HttpResponseRedirect(reverse('error'))
        # Save the changes
    db.commit()

    # disconnect from server
    db.close()

    return HttpResponseRedirect(reverse('references'))


def export_media(request):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    media_cursor = db.cursor()
    media_cursor.execute("SELECT * FROM Media")
    media_data = media_cursor.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="media.csv"'

    writer = csv.writer(response)
    writer.writerow(['MediaID', 'MediaName', 'Year', 'Type',
                     'Genre', 'Description', 'MPAA Rating', 'Critic Rating'])
    for row in media_data:
        writer.writerow(row)

    return response


def export_actors(request):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    media_cursor = db.cursor()
    media_cursor.execute("SELECT * FROM Actor")
    media_data = media_cursor.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="actors.csv"'

    writer = csv.writer(response)
    writer.writerow(['ActorID', 'FirstN', 'MiddleN', 'LastN',
                     'Date Of Birth', 'Gender', 'Birth Country', 'Birth City'])
    for row in media_data:
        writer.writerow(row)

    return response


def export_crews(request):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    media_cursor = db.cursor()
    media_cursor.execute("SELECT * FROM Crew")
    media_data = media_cursor.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="crews.csv"'

    writer = csv.writer(response)
    writer.writerow(['CrewID', 'FirstN', 'MiddleN',
                     'LastN', 'Date of Birth', 'Crew Type'])
    for row in media_data:
        writer.writerow(row)

    return response


def export_meme(request):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    media_cursor = db.cursor()
    media_cursor.execute("SELECT * FROM Memes")
    media_data = media_cursor.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="memes.csv"'

    writer = csv.writer(response)
    writer.writerow(['MemeID', 'Genre', 'Format', 'Description'])
    for row in media_data:
        writer.writerow(row)

    return response


def export_review(request):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    media_cursor = db.cursor()
    media_cursor.execute("SELECT * FROM Review")
    media_data = media_cursor.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reviews.csv"'

    writer = csv.writer(response)
    writer.writerow(['ReviewID', 'MediaID', 'Rating', 'Description'])
    for row in media_data:
        writer.writerow(row)

    return response


def export_refs(request):
    user = request.COOKIES.get('user')
    if(not user):
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie("user")
        return response

    db = pymysql.connect("mysql.cs.virginia.edu",
                         db_user, "ib5pW8ZR", "ceb4aq")

    media_cursor = db.cursor()
    media_cursor.execute("SELECT * FROM Refers")
    media_data = media_cursor.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="references.csv"'

    writer = csv.writer(response)
    writer.writerow(['ReferenceID', 'ReferencerID',
                     'ReferenceeID', 'Description'])
    for row in media_data:
        writer.writerow(row)

    return response
