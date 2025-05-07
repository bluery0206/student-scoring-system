from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator, MinLengthValidator, FileExtensionValidator

from . import models


class SignUpForm(UserCreationForm):
    """ User Registration Form """

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
        """ Metadata """

        # save it to the model
        # Whenever this forms validates, this is going to create a new User
        model = User

        # fields are going to be shown on our form and in what order
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']



class SignInForm(AuthenticationForm):
    """ Login Form"""

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
        """ Metadata """

        model 	= User
        fields 	= ['username', 'password']


class CourseForm(forms.ModelForm):
    """ Login Form"""

    name = forms.CharField(
        widget = forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "[1-A] Introduction to Programming",
        })
    )
    description = forms.CharField(
        widget = forms.Textarea(attrs={
            'class' : 'form-control',
            'placeholder': "Your password",
            'rows': 2,
        }),
        required=False
    )
    instructor = forms.ChoiceField(
        widget = forms.Select(attrs={
            'class' : 'form-control',
        })
    )

    class Meta:
        """ Metadata """

        model 	= models.Course
        fields 	= ["name" ,"description" ,"instructor"]


class SectionForm(forms.ModelForm):
    """ Login Form"""

    name = forms.CharField(
        widget = forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "1-A",
        })
    )
    description = forms.CharField(
        widget = forms.Textarea(attrs={
            'class' : 'form-control',
            'placeholder': "First Year, Section A",
            'rows': 2,
        }),
        required=False
    )

    class Meta:
        """ Metadata """

        model 	= models.Section
        fields 	= ["name" ,"description"]


class StudentForm(forms.ModelForm):
    """ Login Form"""

    first_name = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z-\s]+$',
                message = "Letters and dash only."
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
                r'^[a-zA-Z-\s]+$',
                message = "Letters and dash only."
            )
        ],
        widget = forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "Dela Cruz",
        })
    )
    suffix = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z-\s]+$',
                message = "Letters and dash only."
            )
        ],
        widget = forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "Jr.",
        })
    )
    sex = forms.ChoiceField(
        widget = forms.Select(attrs={
            'class' : 'form-control',
        })
    )
    section = forms.ChoiceField(
        widget = forms.Select(attrs={
            'class' : 'form-control',
        })
    )

    class Meta:
        """ Metadata """

        model 	= models.Student
        fields 	= ["first_name" ,"last_name" ,"suffix", "sex", "section"]



class SectionForm(forms.ModelForm):
    """ Login Form"""

    name = forms.CharField(
        validators = [
            RegexValidator(
                r'^[0-9a-zA-Z\s-]+$',
                message = "Letters and dash only."
            )
        ],
        widget = forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "1-A",
        })
    )
    description = forms.CharField(
        widget = forms.Textarea(attrs={
            'class' : 'form-control',
            'placeholder': "First Year, Section A",
            'rows': 2,
        }),
        required=False
    )

    class Meta:
        """ Metadata """

        model 	= models.Section
        fields 	= ["name" ,"description"]


class TestForm(forms.ModelForm):
    """ Login Form"""

    name = forms.CharField(
        widget = forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "Final Examination",
        })
    )
    description = forms.CharField(
        widget = forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "Final Examination in This Course.",
            'rows': 2,
        }),
        required=False
    )
    total_score = forms.IntegerField(
        widget = forms.NumberInput(attrs={
            'class' : 'form-control',
            'min': 0,
            'max': 100,
        })
    )
    course = forms.ChoiceField(
        widget = forms.Select(attrs={
            'class' : 'form-control',
        })
    )

    class Meta:
        """ Metadata """

        model 	= models.Test
        fields 	= ["name" ,"description" ,"course"]


class ScoreForm(forms.ModelForm):
    """ Login Form"""

    score = forms.IntegerField(
        widget = forms.NumberInput(attrs={
            'class' : 'form-control',
            'min': 0,
            'max': 100,
        })
    )
    student = forms.ChoiceField(
        widget = forms.Select(attrs={
            'class' : 'form-control',
        })
    )
    test = forms.ChoiceField(
        widget = forms.Select(attrs={
            'class' : 'form-control',
        })
    )

    class Meta:
        """ Metadata """

        model 	= models.Score
        fields 	= ["score" ,"student" ,"test"]