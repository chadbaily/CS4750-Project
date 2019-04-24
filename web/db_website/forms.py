from django import forms


class Person(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    middle_name = forms.CharField(
        label='Middle name', max_length=100, required=False)
    last_name = forms.CharField(label='Last name', max_length=100)
    gender = forms.CharField(label='Gender', max_length=6)
    dob = forms.CharField(label='Date of Birth', max_length=10)
    birth_country = forms.CharField(label='Country', max_length=50)
    birth_city = forms.CharField(label='City', max_length=50)


class Crew(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    middle_name = forms.CharField(
        label='Middle name', max_length=100, required=False)
    last_name = forms.CharField(label='Last name', max_length=100)
    ctype = forms.CharField(label='Type', max_length=100)
    dob = forms.CharField(label='Date of Birth', max_length=10)


class Media(forms.Form):
    media_name = forms.CharField(label='Media Type', max_length=100)
    year = forms.CharField(label='Year', max_length=100)
    mtype = forms.CharField(label='type', max_length=100)
    genre = forms.CharField(label='genre', max_length=100)
    description = forms.CharField(
        label='description', max_length=1000, widget=forms.Textarea)
    mpaa_rating = forms.CharField(label='rating', max_length=100)
    crit_rating = forms.CharField(label='crit rating', max_length=100)


class Meme(forms.Form):
    genre = forms.CharField(label='genre', max_length=100)
    description = forms.CharField(
        label='description', max_length=1000, widget=forms.Textarea)
    meme_format = forms.CharField(label='format', max_length=100)


class Login(forms.Form):
    user_name = forms.CharField(label='User name', max_length=100)
    password = forms.CharField(label='Password', max_length=100)


class Review(forms.Form):
    media_id = forms.CharField(label='meda_id', max_length=100)
    rating = forms.CharField(label='review_name', max_length=100)
    description = forms.CharField(
        label='description', max_length=1000, widget=forms.Textarea)


class Reference(forms.Form):
    referencer = forms.CharField(label='referencer', max_length=100)
    referencee = forms.CharField(label='referencee', max_length=100)
    location = forms.CharField(label='location', max_length=100)
    description = forms.CharField(
        label='description', max_length=1000, widget=forms.Textarea)
