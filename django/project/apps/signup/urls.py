from django.urls import path
from . import views


urlpatterns = [
    path('', views.signin, name='sign'),
    path('login/', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('register/', views.signup, name='signup'),
]
