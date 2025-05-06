from django.urls import path, include
from . import views


authpatterns = [
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signout/', views.signout, name="signout"),
]

urlpatterns = [
    path('', views.index, name="app-index"),
    path('auth/', include((authpatterns, 'auth'))),
]
