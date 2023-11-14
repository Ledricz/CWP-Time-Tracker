import json

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Employees


class UsersAPITestCase(APITestCase):
    test_data = {
        "first_name": "Tyler",
        "last_name": "Doe",
        "email": "tylerdoe@example.com",
        "password": "1234",
    }

    def test_create_user(self):
        response = self.client.post("/api/v1/employees/", json.dumps(self.test_data), content_type="application/json")
        test_user = Employees.objects.get(pk=response.data.get("id"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_users(self):
        test_user = Employees.objects.create(**self.test_data)
        test_user.save()

        response = self.client.get(f"/api/v1/employees/", content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("first_name"), self.test_data.get("first_name"))
        self.assertEqual(response.data[0].get("last_name"), self.test_data.get("last_name"))
        self.assertEqual(response.data[0].get("email"), self.test_data.get("email"))

    def test_update_user(self):
        test_user = Employees.objects.create(**self.test_data)
        test_user.save()

        data = {
            "first_name": "Mark",
            "last_name": "Whiteman"
        }
        response = self.client.patch(f"/api/v1/employees/{test_user.pk}/", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("first_name"), "Mark")
        self.assertEqual(response.data.get("last_name"), "Whiteman")
