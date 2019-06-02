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

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index),
    path('header.html', views.header),
    path('faculties/<str:faculty>', views.faculties),
    path('faculties/<str:faculty>/groups/<str:group>', views.groups),
    path('faculties/<str:faculty>/groups/<str:group>/students/<str:student_id>', views.students),
    path('buildings/<str:building>', views.buildings),
    path('buildings/<str:building>/auditoriums/<str:auditorium>/date/<str:date>/index/<int:index>', views.lessons),
    
    path('dategate', datagate.views.lowlevel),
]
