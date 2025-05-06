from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote # For decoding encoded urls (e.g. https%3A%2F%2Fexample.com -> https://example.com)

import logging

from .forms import (
    SignUpForm, 
    SignInForm, 
)



logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@login_required
def index(request):
    """ Shows the index/home/dashboard page """

    context = {
    #     'form': UserRegisterForm()
    }

    return render(request, "app/index.html", context)



def signin(request):
    """ User Login View """

    form = SignInForm()

    if request.method == "POST":
        form = SignInForm(request, data=request.POST)
        logger.debug("User's credentials accepted. Validating...")

        if form.is_valid():
            logger.debug("User's credentials are VALID. Logging in...")
            login(request, form.get_user())
            output_msg = f"User ({form.get_user().username}) successfuly signed in."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect('app-index')

    context = {
        'title': 'Sign In',
        'form': form,
    }

    return render(request, "app/auth/signin.html", context)


def signup(request):
    """ User Register View """

    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            instance = form.save()
            msg = f"User ({instance.user.get_user().username}) successfully created."
            messages.success(request, msg)
            logger.debug(msg)
            return redirect('auth:signin')

    context = {
        'title': 'Sign Up',
        'form': form,
    }

    return render(request, "app/auth/signup.html", context)


def signout(request):
    """ Logouts the user """
    user = request.user
    logout(request)
    output_msg = f"User ({user.username}) successfuly signed out."
    logger.debug(output_msg)
    messages.success(request, output_msg)
    return redirect('app-index')
