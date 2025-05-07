from django.urls import path, include
from . import views


authpatterns = [
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signout/', views.signout, name="signout"),
]

testpatterns = [
    path('add/', views.test_add, name="add"),
    path('edit/<int:test_id>/', views.test_edit, name="edit"),
    path('delete/<int:test_id>/', views.test_delete, name="delete"),
    path('delete/all/', views.test_delete_all, name="delete_all"),
    path('<int:test_id>/', views.test_view, name="view"),
]

coursepatterns = [
    path('', views.course, name="index"),
    path('add/', views.course_add, name="add"),
    path('edit/<int:course_id>/', views.course_edit, name="edit"),
    path('delete/<int:course_id>/', views.course_delete, name="delete"),
    path('delete/all/', views.course_delete_all, name="delete_all"),
    path('view/<int:course_id>/', views.course_view, name="view"),
    
    path('view/<int:course_id>/test/', include((testpatterns, 'test'))),
]

studentpatterns = [
    path('add/', views.student_add, name="add"),
    path('edit/<int:student_id>/', views.student_edit, name="edit"),
    path('delete/<int:student_id>/', views.student_delete, name="delete"),
    path('delete/all/', views.student_delete_all, name="delete_all"),
    path('<int:student_id>/', views.student_view, name="view"),
]

sectionpatterns = [
    path('', views.section, name="index"),
    path('add/', views.section_add, name="add"),
    path('edit/<int:pk>', views.section_edit, name="edit"),
    path('delete/<int:pk>/', views.section_delete, name="delete"),
    path('delete/all/', views.section_delete_all, name="delete_all"),
    path('view/<int:pk>/', views.section_view, name="view"),

    path('view/<int:section_id>/student/', include((studentpatterns, 'student'))),
]

urlpatterns = [
    path('', views.index, name="app-index"),
    path('auth/', include((authpatterns, 'auth'))),
    path('course/', include((coursepatterns, 'course'))),
    path('section/', include((sectionpatterns, 'section'))),
]
