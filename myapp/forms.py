from django import forms
from django.contrib.auth.models import User
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        strip=False,
        required=True,
        help_text='',
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput,
        strip=False,
        required=True,
        # help_text="Your password must contain at least 8 characters.",
        error_messages={
            'password_mismatch': "The two password fields didn't match.",
        },
        )
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password']:
            raise forms.ValidationError('Password does not match')
        return cd['password2']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can customize the form widget attributes here if needed
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'rows': 3})
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ["user", "message"]

