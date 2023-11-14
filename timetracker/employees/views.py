from django.contrib.auth import login, logout

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Employees
from .serializers import EmployeesSerializer


class EmployeesViewSet(ModelViewSet):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    
    @action(detail=False, methods=["POST"])
    def signup_login(self, request, pk=None):
        self.create(request, pk)
        return self.login(request, pk)    
    
    @action(detail=True, methods=["PATCH"])
    def update_login(self, request, pk=None):
        self.update(request, pk)
        return self.login(request, pk)

    @action(detail=False, methods=["POST"])
    def login(self, request, pk=None):
        if not request.data.get("email"):
            raise ValidationError("This field is required")
        if not request.data.get("password"):
            raise ValidationError("This field is required")
        
        user = self.serializer_class().check_user(request.data)
        if not user and pk:            
            user = self.queryset.get(pk=pk)
        if user:
            login(request, user)
            return Response({"id": user.id, "name": user.name}, status=status.HTTP_200_OK)
        
        return Response({"message": "Invalid email or pin code"}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False)
    def logout(self, request, pk=None):
        logout(request)        
        return Response(status=status.HTTP_200_OK)
