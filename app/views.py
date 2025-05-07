from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote # For decoding encoded urls (e.g. https%3A%2F%2Fexample.com -> https://example.com)

import logging

from . import forms
from . import models



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

    form = forms.SignInForm()

    if request.method == "POST":
        form = forms.SignInForm(request, data=request.POST)
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

    form = forms.SignUpForm()

    if request.method == "POST":
        form = forms.SignUpForm(request.POST)

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


def course(request):

    context = {
        'title': 'Courses',
    }

    return render(request, "app/course/index.html", context)


def course_add(request):

    context = {
        'title': 'Course - Add',
    }

    return render(request, "app/course/index.html", context)


def course_edit(request, pk):

    context = {
        'title': 'Course - edit',
    }

    return render(request, "app/course/index.html", context)

def course_delete(request, pk):

    context = {
        'title': 'Course - Delete',
    }

    return render(request, "app/course/index.html", context)

def course_delete_all(request):

    context = {
        'title': 'Course - Delete',
    }

    return render(request, "app/course/index.html", context)


def section(request):
    sections = models.Section.objects.all()

    context = {
        'title': 'Sections',
        'sections': sections,
    }

    return render(request, "app/section/index.html", context)


def section_add(request):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        form = forms.SectionForm(request.POST)
        logger.debug("Section accepted. Validating...")

        if form.is_valid():
            form.save()
            output_msg = f"Section ({form.instance.name}) created."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect(next if next else 'section:index')
    else:
        form = forms.SectionForm()

    context = {
        'title': 'Section - Add',
        'form': form,
        'is_desctructive': False,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/section/form.html", context)


def section_edit(request, pk):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    section = get_object_or_404(models.Section, pk=pk)

    if request.method == "POST":
        form = forms.SectionForm(request.POST, instance=section)

        if form.is_valid():
            form.save()
            output_msg = f"Section ({form.instance.name}) edited successfully."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect(next if next else 'section:index')
    else:
        form = forms.SectionForm(instance=section)

    context = {
        'title': f'Section - Edit {section.name}',
        'form': form,
        'is_desctructive': False,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/section/form.html", context)

def section_delete(request, pk):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    section = get_object_or_404(models.Section, pk=pk)
    name = section.name 

    if request.method == "POST":
        section.delete()
        output_msg = f"Section ({name}) deleted successfully."
        logger.debug(output_msg)
        messages.success(request, output_msg)
        return redirect(next if next else 'section:index')
    
    context = {
        'title': f'Section - Delete {name}',
        'description': "This operation cannot be undone.",
        'is_desctructive': True,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/base/form.html", context)


def section_delete_all(request):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        sections = models.Section.objects.all()
        logger.debug("Deleting sections")

        for section in sections:
            section.delete()

        output_msg = f"All sections deleted successfully."
        logger.debug(output_msg)
        messages.success(request, output_msg)
        return redirect(next if next else 'section:index')
    
    context = {
        'title': f'Section - Delete All',
        'description': "This operation cannot be undone.",
        'is_desctructive': True,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/base/form.html", context)
