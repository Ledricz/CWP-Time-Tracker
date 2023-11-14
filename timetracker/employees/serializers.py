import re

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Employees


class EmployeesSerializer(serializers.ModelSerializer):

	def validate_password(self, value):
		errors = []
		if not value.isnumeric():
			errors.append(serializers.ValidationError("Pin code should only contain digits"))
		if len(value) != 4:
			errors.append(serializers.ValidationError("Pin code should be 4 characters long"))
		
		
		if errors:
			raise serializers.ValidationError(errors)
		
		return value
	
	def create(self, data):
		user = Employees.objects.create(
			first_name=data['first_name'],
			last_name=data['last_name'],
			email=data['email']
		)
		user.set_password(data['password'])
		user.save()
		return user
	
	def check_user(self, data):
		return authenticate(email=data.get("email"), password=data.get("password"))
	
	class Meta:
		model = Employees
		fields = "__all__"
