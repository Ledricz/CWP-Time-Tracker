import json

from django.shortcuts import render
from django.http.request import QueryDict

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


from timetracker.functions import get_week, get_weekly_table

from .models import Projects, Entries
from .serializers import ProjectsSerializer, EntriesSerializer


class EntriesViewSet(ModelViewSet):
    queryset = Entries.objects.all()
    serializer_class = EntriesSerializer
    
    @action(detail=True)
    def get_weekly_table(self, request, pk=None, week=None):   
        if pk is None:
            raise ValidationError("Logged-in User is required")
        if week is None:
            week = request.query_params.get("week", 0)

        data = get_weekly_table(user_id=pk, week_num=week)
        data["week_num"] = week
        return Response(data=data, status=status.HTTP_200_OK)


    @action(detail=False)
    def get_week(self, request):
        week = request.query_params.get("week")
        weekdates = get_week(week=week)
        return Response({"weekdates": weekdates}, status=status.HTTP_200_OK)

class ProjectsViewSet(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if "data" in request.data:
            data = json.loads(request.data.get("data"))

        is_many = isinstance(data, list)
        serializer = self.serializer_class(data=data, many=is_many)            
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    @action(detail=False)
    def add_new_line(self, request, pk=None):
        html_content = render(request, "snippets/add_new_project_line.html", {"data": ""})
        return html_content