"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
import datagate.views
import integration.views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index),
    path('header.html', views.header, name='website-header'),
    path('faculties/<str:faculty>', views.faculties),
    path('faculties/<str:faculty>/groups/<str:group>', views.groups),
    path('faculties/<str:faculty>/groups/<str:group>/students/<str:student_id>', views.students),
    path('buildings/<str:building>', views.buildings),
    path('buildings/<str:building>/auditoriums/<str:auditorium>/date/<str:date>/index/<int:index>', views.Lessons.as_view()),
    
    path('login', views.Login.as_view()),
    path('logout', views.logout),

    path('professor', views.professors_lessons),
    path('dean', views.Dean.as_view()),

    path('dategate', datagate.views.lowlevel),

    path('integration', integration.views.integrationPreview),
    path('run_integration', integration.views.Integration.as_view()),
]
