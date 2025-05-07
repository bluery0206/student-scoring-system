from django.contrib import admin
from . import models

admin.site.register([
    models.Course,
    models.Section,
    models.Student,
    models.Test,
    models.Score,
])