from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator, MinLengthValidator, FileExtensionValidator

from . import models


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget = forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "example@domain.com",
                'minlength': 4,
        }),
    )
    username = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z0-9_.]{4,}$',
                message = "Letters, numbers, underscore, and period only."
            )
        ],
        widget = forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "example_example02",
        })
    )
    first_name = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z\s]+$',
                message = "Letters only."
            )
        ],
        widget = forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "Juan",
        })
    )
    last_name = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z\s]+$',
                message = "Letters only."
            )
        ],
        widget = forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "Dela Cruz",
        })
    )
    password1 = forms.CharField(
        validators = [
            MinLengthValidator(8)
        ],
        widget = forms.PasswordInput(attrs={
                'class' : 'form-control',
                'placeholder': "Must have at least 8 characters",
        })
    )
    password2 = forms.CharField(
        validators = [
            MinLengthValidator(8)
        ],
        widget = forms.PasswordInput(attrs={
                'class' : 'form-control',
                'placeholder': "Must have at least 8 characters",
        })
    )

    class Meta:
        # save it to the model
        # Whenever this forms validates, this is going to create a new User
        model = User

        # fields are going to be shown on our form and in what order
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z0-9_.]+$',
                message = "Letters, numbers, underscore, and period only."
            )
        ],
        widget = forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "example_example02",
        })
    )
    password = forms.CharField(
        widget = forms.PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder': "Your password",
        })
    )

    class Meta:
        model 	= User
        fields 	= ['username', 'password']


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ["name" ,"description" , "section"]
        widgets = {
            "name" :forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "[1-A] Introduction to Programming",
            }),
            "description": forms.Textarea(attrs={
                'class' : 'form-control',
                'placeholder': "This course is brought to you by...",
                'rows': 2,
            }),
            "section": forms.Select(attrs={
                'class': 'form-control'
            })
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model 	= models.Section
        fields 	= ["name" ,"description"]
        widgets = {
            "name": forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "1-A",
            }),
            "description": forms.Textarea(attrs={
                'class' : 'form-control',
                'placeholder': "First Year, Section A",
                'rows': 2,
            }),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model 	= models.Student
        fields 	= ["first_name" ,"last_name" ,"suffix", "sex", "section"]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "Juan",
            }),
            'last_name': forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "Dela Cruz",
            }),
            "suffix": forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "Jr.",
            }),
            "sex": forms.Select(attrs={
                'class' : 'form-control',
            }),
            "section": forms.Select(attrs={
                'class' : 'form-control',
            }),
        }



class SectionForm(forms.ModelForm):
    class Meta:
        model 	= models.Section
        fields 	= ["name" ,"description"]
        widgets = {
            "name": forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "1-A",
            }),
            "description": forms.Textarea(attrs={
                'class' : 'form-control',
                'placeholder': "First Year, Section A",
                'rows': 2,
            }),
        }


class TestForm(forms.ModelForm):
    class Meta:
        model 	= models.Test
        fields 	= ["name" ,"description" ,"course"]
        widgets = {
            "name": forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "Final Examination",
            }),
            "description": forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "Final Examination in This Course.",
                'rows': 2,
            }),
            "total_score": forms.NumberInput(attrs={
                'class' : 'form-control',
                'min': 0,
                'max': 100,
            }),
            "course": forms.Select(attrs={
                'class' : 'form-control',
            })
        }


class ScoreForm(forms.ModelForm):
    class Meta:
        model 	= models.Score
        fields 	= ["score" ,"student" ,"test"]
        widgets = {
            "score": forms.NumberInput(attrs={
                'class' : 'form-control',
                'min': 0,
                'max': 100,
            }),
            "student": forms.Select(attrs={
                'class' : 'form-control',
            }),
            "test": forms.Select(attrs={
                'class' : 'form-control',
            }),
        }