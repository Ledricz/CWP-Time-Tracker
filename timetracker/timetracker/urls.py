"""
URL configuration for timetracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect

from frontend.views import HomeAPIView, SignInAPIView, LogInAPIView, EmployeesAPIView, ProjectsAPIView, EntriesAPIView

urlpatterns = [
    path('', lambda req: redirect("home/")),
    path('home/', HomeAPIView.as_view(), name="home"),
    path('signin/', SignInAPIView.as_view(), name="signin"),
    path('login/', LogInAPIView.as_view(), name="login"),
    path('employees/', EmployeesAPIView.as_view(), name="employees"),
    path('projects/', ProjectsAPIView.as_view(), name="projects"),
    path('timesheets/<int:user_id>/', EntriesAPIView.as_view(), name="timesheets"),
    path('timesheets/<int:user_id>/week/<slug:week>/', EntriesAPIView.as_view(), name="timesheets"),
    path('api/v1/', include('employees.urls')),
    path('api/v1/', include('timesheets.urls')),
]
