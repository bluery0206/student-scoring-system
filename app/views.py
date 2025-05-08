from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote # For decoding encoded urls (e.g. https%3A%2F%2Fexample.com -> https://example.com)

import logging
import numpy as np
import json as js

from . import forms
from . import models



logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@login_required
def index(request):
    courses = models.Course.objects.all()[:9]
    sections = models.Section.objects.all()[:6]
    tests = models.Test.objects.all()[:6]

    context = {
        "courses": courses,
        "sections": sections,
        "tests": tests,
        "current_url": request.build_absolute_uri,
    }

    return render(request, "app/index.html", context)



def signin(request):
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
    user = request.user
    logout(request)
    output_msg = f"User ({user.username}) successfuly signed out."
    logger.debug(output_msg)
    messages.success(request, output_msg)
    return redirect('app-index')



def course(request):
    courses = models.Course.objects.filter(instructor=request.user)

    context = {
        'title': 'Courses',
        'courses': courses,
    }

    return render(request, "app/course/index.html", context)



def course_add(request):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        form = forms.CourseForm(request.POST)
        logger.debug("Section accepted. Validating...")

        if form.is_valid():
            instance = form.save(commit=False)
            instance.instructor = request.user
            instance.save()
            output_msg = f"Section ({form.instance.name}) created."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect(next if next else 'course:index')
    else:
        form = forms.CourseForm()

    context = {
        'title': 'Course - Add',
        'form': form,
        'is_desctructive': False,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/course/form.html", context)



def course_edit(request, course_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    course = get_object_or_404(models.Course, pk=course_id)

    if request.method == "POST":
        form = forms.CourseForm(request.POST, instance=course)

        if form.is_valid():
            form.save()
            output_msg = f"Course ({form.instance.name}) edited successfully."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect(next if next else 'course:index')
    else:
        form = forms.CourseForm(instance=course)

    context = {
        'title': f'Course - Edit {course.name}',
        'form': form,
        'is_desctructive': False,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/course/form.html", context)



def course_delete(request, course_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    course = get_object_or_404(models.Course, pk=course_id)
    name = course.name 

    if request.method == "POST":
        course.delete()
        output_msg = f"Course ({name}) deleted successfully."
        logger.debug(output_msg)
        messages.success(request, output_msg)
        return redirect(next if next else 'course:index')
    
    context = {
        'title': f'Course - Delete {name}',
        'description': "This operation cannot be undone.",
        'is_desctructive': True,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/base/form.html", context)



def course_delete_all(request):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        courses = models.Course.objects.all()
        logger.debug("Deleting courses")

        for course in courses:
            course.delete()

        output_msg = f"All courses deleted successfully."
        logger.debug(output_msg)
        messages.success(request, output_msg)
        return redirect(next if next else 'course:index')
    
    context = {
        'title': f'Course - Delete All',
        'description': "This operation cannot be undone.",
        'is_desctructive': True,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/base/form.html", context)



def course_view(request, course_id):
    course = get_object_or_404(models.Course, pk=course_id)
    section = course.section
    students = section.students.all()
    tests = course.tests.all()

    context = {
        'title': f'Course - {course.name}',
        'course': course,
        'section': section,
        'tests': tests,
        'students': students,
    }

    return render(request, "app/course/view.html", context)



def section(request):
    sections = models.Section.objects.all()

    context = {
        'title': 'Sections',
        'sections': sections,
        "current_url": request.build_absolute_uri,
    }

    return render(request, "app/section/index.html", context)



def section_add(request):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        form = forms.SectionForm(request.POST)

        if form.is_valid():
            form.save()
            output_msg = f"Section ({form.instance.name}) succesfully created."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect(next if next else 'section:index')
    else:
        form = forms.SectionForm()

    context = {
        'title': 'Section - Add',
        'form': form,
        'prev': prev,
        "current_url": request.build_absolute_uri,
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
        'prev': prev,
        "current_url": request.build_absolute_uri,
    }

    return render(request, "app/section/form.html", context)



def section_delete(request, pk):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    section = get_object_or_404(models.Section, pk=pk)
    section_name = section.name 
    
    if request.method == "POST":
        output_msg = f"Section ({section_name}) deleted successfully."
        section.delete()
        logger.debug(output_msg)
        messages.success(request, output_msg)
        return redirect(next if next else 'section:index')
    
    context = {
        'title': f'Section - Delete {section_name}',
        'description': "This operation cannot be undone. All students that belongs to this section will also be deleted.",
        'is_desctructive': True,
        'prev': prev,
        'next': next,
        "current_url": request.build_absolute_uri,
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

        output_msg = "All sections deleted successfully."
        logger.debug(output_msg)
        messages.success(request, output_msg)
        return redirect(next if next else 'section:index')
    
    context = {
        'title': f'Section - Delete All',
        'description': "This operation cannot be undone. All students within sections will also be deleted.",
        'is_desctructive': True,
        'prev': prev,
        "current_url": request.build_absolute_uri,
    }

    return render(request, "app/base/form.html", context)



def section_view(request, pk):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))
    
    section = get_object_or_404(models.Section, pk=pk)
    students = section.students.all()

    context = {
        'title': f'Section - {section.name}',
        'section': section,
        'students': students,
        'prev': prev,
        "current_url": request.build_absolute_uri,
    }

    return render(request, "app/section/view.html", context)









def student_add(request, section_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    section = get_object_or_404(models.Section, pk=section_id)

    if request.method == "POST":
        form = forms.StudentForm(request.POST)
        logger.debug("Student accepted. Validating...")

        if form.is_valid():
            instance = form.save(commit=False)
            instance.section = section
            instance.save()
            output_msg = f"Student ({form.instance.full_name}) created."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect(next if next else 'student:index')
    else:
        form = forms.StudentForm()

    context = {
        'title': 'Student - Add',
        'form': form,
        'section': section,
        'is_desctructive': False,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/student/form.html", context)


def student_edit(request, section_id, student_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    section = get_object_or_404(models.Section, pk=section_id)
    student = get_object_or_404(models.Student, pk=student_id)

    if request.method == "POST":
        form = forms.StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            output_msg = f"Student ({form.instance.full_name}) edited successfully."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect(next if next else 'section:index')
    else:
        form = forms.StudentForm(instance=student)

    context = {
        'title': f'Student - Edit {student.full_name}',
        'form': form,
        'section': section,
        'is_desctructive': False,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/student/form.html", context)

def student_delete(request, section_id, student_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    student = get_object_or_404(models.Student, pk=student_id)
    name = student.full_name 

    if request.method == "POST":
        student.delete()
        output_msg = f"Student ({name}) deleted successfully."
        logger.debug(output_msg)
        messages.success(request, output_msg)
        return redirect(next if next else 'section:index')
    
    context = {
        'title': f'Student - Delete {name}',
        'description': "This operation cannot be undone.",
        'is_desctructive': True,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/base/form.html", context)


def student_delete_all(request, section_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        section = get_object_or_404(models.Section, pk=section_id)
        students = section.students.all()
        logger.debug("Deleting students")

        for student in students:
            student.delete()

        output_msg = f"All student deleted successfully."
        logger.debug(output_msg)
        messages.success(request, output_msg)
        return redirect(next if next else 'student:index')
    
    context = {
        'title': f'Student - Delete All',
        'description': "This operation cannot be undone.",
        'is_desctructive': True,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/base/form.html", context)

def student_view(request, section_id, student_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))
    
    student = get_object_or_404(models.Student, pk=student_id)
    section = get_object_or_404(models.Section, pk=section_id)

    context = {
        'title': f'Student - {student.full_name}',
        'student': student,
        'section': section,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/student/view.html", context)














def test_add(request, course_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    course = get_object_or_404(models.Course, pk=course_id)

    if request.method == "POST":
        form = forms.TestForm(request.POST)
        logger.debug("test accepted. Validating...")

        if form.is_valid():
            print("YEAHH")
            instance = form.save(commit=False)
            instance.course = course
            instance.save()
            output_msg = f"test ({form.instance.name}) created."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect(next if next else 'course:index')
    else:
        form = forms.TestForm()

    context = {
        'title': 'Test - Add',
        'form': form,
        'course': course,
        'is_desctructive': False,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/test/form.html", context)


def test_edit(request, course_id, test_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    course = get_object_or_404(models.Course, pk=course_id)
    test = get_object_or_404(models.Test, pk=test_id)

    if request.method == "POST":
        form = forms.TestForm(request.POST, instance=test)

        if form.is_valid():
            form.save()
            output_msg = f"Test ({form.instance.name}) edited successfully."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect(next if next else 'course:index')
    else:
        form = forms.TestForm(instance=test)

    context = {
        'title': f'test - Edit {test.name}',
        'form': form,
        'course': course,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/test/form.html", context)

def test_delete(request, course_id, test_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    test = get_object_or_404(models.Test, pk=test_id)
    name = test.name 

    if request.method == "POST":
        test.delete()
        output_msg = f"Test ({name}) deleted successfully."
        logger.debug(output_msg)
        messages.success(request, output_msg)
        return redirect(next if next else 'course:index')
    
    context = {
        'title': f'Test - Delete {name}',
        'description': "This operation cannot be undone.",
        'is_desctructive': True,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/base/form.html", context)


def test_delete_all(request, course_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        course = get_object_or_404(models.Course, pk=course_id)
        tests = course.tests.all()
        logger.debug("Deleting tests")

        for test in tests:
            test.delete()

        output_msg = f"All tests deleted successfully."
        logger.debug(output_msg)
        messages.success(request, output_msg)
        return redirect(next if next else 'course:index')
    
    context = {
        'title': f'Test - Delete All',
        'description': "This operation cannot be undone.",
        'is_desctructive': True,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/base/form.html", context)

def test_view(request, course_id, test_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))
    
    test:models.Test = get_object_or_404(models.Test, pk=test_id)
    course = get_object_or_404(models.Course, pk=course_id)
    section = course.section
    students:list[models.Student] = section.students.all()

    # Get all student score instances
    scores = [student.scores.filter(test=test).first() for student in students]

    # Getting score values and if None if score instance is NOne
    scores_list = [(None if not score else score.score) for score in scores]

    # Plus one para naay perfect nga score
    total_score = test.total_score + 1

    # a list [0, ..., total_score]
    scores_range = list(range(total_score))

    # Inits an array to count how many scores exists
    scores_freq = [0 for _ in range(total_score)]

    # Counts the scores
    for score in scores_list: 
        if type(score) == int:
            scores_freq[score] += 1

    # Tungaon ang list N_SPLIT times para dile kaayo guot sa graph
    N_SPLIT = 10
    scores_freq = np.array_split(scores_freq, N_SPLIT)
    scores_range = np.array_split(scores_range, N_SPLIT)

    # Kuhaon ang first number ug ang last number sa kada split 
    # Then convert to string so "start_number-end_number"
    scores_range = [str(f"{score[0]}-{score[-1]}") for score in scores_range]

    # I total tanang number kada split
    scores_freq = [int(score.sum()) for score in scores_freq]

    # GETTING THE PERCENTAGE OF PASSED STUDENT
    n_passed = 0
    n_failed = 0
    # Counts the scores
    for score in scores_list: 
        if type(score) is int:
            if score > test.passing_score:
                n_passed += 1
            else:
                n_failed += 1

    context = {
        'title': f'Test - {test.name}',
        'test': test,
        'course': course,
        'section': section,
        'students': zip(students, scores),
        'scores_freq': js.dumps(scores_freq),
        'scores_range': js.dumps(scores_range),
        'n_passed': js.dumps(n_passed),
        'n_failed': js.dumps(n_failed),
        'prev': prev,
        'next': next,
    }

    return render(request, "app/test/view.html", context)



def score_add(request, course_id, test_id, student_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    course = get_object_or_404(models.Course, pk=course_id)
    test = course.tests.get(id=test_id)
    student = get_object_or_404(models.Student, pk=student_id)

    if request.method == 'POST':
        form = forms.ScoreForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.test = test
            instance.student = student
            instance.save()
            output_msg = f"test ({form.instance}) created."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect(next if next else 'course:index')
    else:
        form = forms.ScoreForm()

    context = {
        'title': 'Score - Add',
        'form': form,
        'course': course,
        'student': student,
        'test': test,
        'is_desctructive': False,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/score/form.html", context)


def score_edit(request, course_id, test_id, student_id, score_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    course = get_object_or_404(models.Course, pk=course_id)
    test = course.tests.get(id=test_id)
    student = get_object_or_404(models.Student, pk=student_id)
    score = get_object_or_404(models.Score, pk=score_id)

    if request.method == 'POST':
        form = forms.ScoreForm(request.POST, instance=score)

        if form.is_valid():
            form.save()
            output_msg = f"test ({form.instance}) created."
            logger.debug(output_msg)
            messages.success(request, output_msg)
            return redirect(next if next else 'course:index')
    else:
        form = forms.ScoreForm(instance=score)

    context = {
        'title': 'Score - Edit',
        'form': form,
        'course': course,
        'student': student,
        'test': test,
        'is_desctructive': False,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/score/form.html", context)



def score_delete(request, course_id, test_id, student_id, score_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    score = get_object_or_404(models.Score, pk=score_id)

    if request.method == 'POST':
        output_msg = f"test ({score}) deleted."
        score.delete()
        logger.debug(output_msg)
        messages.success(request, output_msg)
        return redirect(next if next else 'course:index')

    context = {
        'title': 'Score - Delete',
        'course': course,
        'description': 'This operation cannot be undone',
        'is_desctructive': True,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/score/form.html", context)



def score_delete_all(request, course_id, test_id, student_id):
    prev = unquote(request.GET.get("prev", ""))
    next = unquote(request.GET.get("next", ""))

    if request.method == "POST":
        student = get_object_or_404(models.Student, pk=student_id)
        scores = student.scores.all()
        logger.debug("Deleting scores")

        for score in scores:
            score.delete()

        output_msg = f"All scores deleted successfully."
        logger.debug(output_msg)
        messages.success(request, output_msg)
        return redirect(next if next else 'course:index')
    
    context = {
        'title': f'Score - Delete All',
        'description': "This operation cannot be undone.",
        'is_desctructive': True,
        'prev': prev,
        'next': next,
    }

    return render(request, "app/base/form.html", context)