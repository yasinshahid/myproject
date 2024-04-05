from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, EmailValidator
from .models import Book
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        validators=[MinLengthValidator(8)],
        help_text="Enter a username with at least 8 characters."
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[MinLengthValidator(8)],
        help_text="Enter a password with at least 8 characters, including at least one uppercase letter, lowercase letter, number, and special character."
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None  # Remove help text
        self.fields['password'].help_text = None  # Remove help text

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author','publication_date', 'genre']