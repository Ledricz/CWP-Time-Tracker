from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from timetracker.functions import get_weekly_table

from employees.models import Employees
from timesheets.models import Projects, Entries
from timesheets.views import EntriesViewSet


class HomeAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "home.html"

    def get(self, request):
        return Response({})
    

class SignInAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "register.html"

    def get(self, request):
        return Response({"active_tab": "sign_in"})    


class LogInAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "register.html"

    def get(self, request):
        return Response({"active_tab": "log_in"})
    

class EmployeesAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = "employees.html"

    def get(self, request):
        queryset = Employees.objects.filter(active=True)
        return Response({"employees": queryset})    


class ProjectsAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = "projects.html"

    def get(self, request):
        queryset = Projects.objects.filter(active=True)
        entries = Entries.objects.all()
        employees = Employees.objects.all()

        projects = []
        for project in queryset:
            entries_in_project = entries.filter(project_id=project.id)
            hours, mins = Entries.get_totals(entries_in_project)
            data = {
                "id": project.id,
                "name": project.name,
                "totals": f"{hours:02d}:{mins:02d}",
                "users": []
            }
            users_in_project = employees.filter(pk__in=[entry.user_id.id for entry in entries_in_project])
            for user in users_in_project:
                entries_by_user = entries_in_project.filter(user_id=user.id)
                hours, mins = Entries.get_totals(entries_by_user)
                datum = {
                    "id": user.id,
                    "name": user.name,
                    "total_time": f"{hours:02d}:{mins:02d}",
                }
                data["users"].append(datum)

            projects.append(data)

        return Response({"projects": projects})


class EntriesAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    # permission_classes = [IsAuthenticated]
    template_name = "entries.html"

    def get(self, request, user_id=None, week=None):   
        if user_id is None:
            raise ValidationError("Logged-in User is required")
        if week is None:
            week = request.query_params.get("week", 0)

        data = get_weekly_table(user_id=user_id, week_num=week)
        data["week_num"] = week
        data["all_projects"] = Projects.objects.filter(active=True)
        return Response(data=data)
