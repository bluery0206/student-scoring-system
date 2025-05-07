from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator, FileExtensionValidator



class Section(models.Model):
    name = models.CharField(
        max_length=50, 
        unique=True,
        validators = [
            RegexValidator(
                r'^[0-9a-zA-Z\s-]+$',
                message = "Letters and dash only."
            )
        ],
    )
    description = models.CharField(max_length=200, blank=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
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
            'instructor',
            'section',
        ]]


class Student(models.Model):
    first_name = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^[a-zA-Z-\s]+$',
                message = "Letters and dash only."
            )
        ],
    )
    last_name = models.CharField(
        max_length=20,
        validators = [
            RegexValidator(
                r'^[a-zA-Z-\s]+$',
                message = "Letters and dash only."
            )
        ],
    )
    suffix = models.CharField(
        max_length=20,
        blank=True,
        validators = [
            RegexValidator(
                r'^[a-zA-Z-\s]+$',
                message = "Letters and dash only."
            )
        ],
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
    description = models.CharField(max_length=200, blank=True)
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
