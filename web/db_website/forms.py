from django import forms


class Person(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    middle_name = forms.CharField(
        label='Middle name', max_length=100, required=False)
    last_name = forms.CharField(label='Last name', max_length=100)
    gender = forms.CharField(label='Gender', max_length=6)
    dob = forms.CharField(label='Date of Birth', max_length=10)
