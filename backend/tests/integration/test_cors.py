from rest_framework.test import APIClient
from django.urls import reverse

def test_cors_allows_any_origin(db, api_client: APIClient):
    url = reverse("register")
    data = {"email": "ex@gmail.com", "password": "123", "first_name": "LUka", "last_name": "Mania", "role": "Student"}
    response = api_client.post(url, data, HTTP_ORIGIN="http://example.com", format="json")
    
    assert response.status_code == 201
    assert response["Access-Control-Allow-Origin"] == "*"
