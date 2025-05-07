from django.urls import path, include
from . import views


authpatterns = [
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signout/', views.signout, name="signout"),
]

coursepatterns = [
    path('', views.course, name="index"),
    path('add/', views.course_add, name="add"),
    path('update/<int:pk>', views.course_update, name="update"),
    path('delete/<int:pk>', views.course_delete, name="delete"),
]

sectionpatterns = [
    path('', views.section, name="index"),
    path('add/', views.section_add, name="add"),
    path('update/<int:pk>', views.section_update, name="update"),
    path('delete/<int:pk>', views.section_delete, name="delete"),
]

urlpatterns = [
    path('', views.index, name="app-index"),
    path('auth/', include((authpatterns, 'auth'))),
    path('course/', include((coursepatterns, 'course'))),
    path('section/', include((sectionpatterns, 'section'))),
]
