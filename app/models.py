from django.db import models
from django.contrib.auth.models import User



class Section(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['name', 'description']]
        
class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [[
            'name', 
            'description', 
            'instructor',
            'section',
        ]]


class Student(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    suffix = models.CharField(
        max_length=20,
        blank=True
    )
    sex = models.CharField(
        max_length=1,
        choices=[
            ("m", "Male"),
            ("f", "Female"),
        ],
        default="m",
    )
    section = models.ForeignKey(
        Section, 
        on_delete=models.CASCADE, 
        related_name="students"
    )
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [[
            'first_name', 
            'last_name', 
            'suffix',
            'sex',
        ]]


class Test(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    total_score = models.IntegerField(default=0)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name="tests"
    )
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [[
            'name', 
            'description', 
            'total_score',
            'course',
        ]]


class Score(models.Model):
    score = models.SmallIntegerField(default=0)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="scores"
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="scores"
    )
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [[
            'score', 
            'student', 
            'test',
        ]]
