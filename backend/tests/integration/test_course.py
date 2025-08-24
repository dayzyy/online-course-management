import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from domain.models import CustomUser, Course

@pytest.fixture
def teacher_user(db):
    return CustomUser.objects.create_user(
        email="teacher@example.com",
        password="password123",
        first_name="Teacher",
        last_name="Example",
        role=CustomUser.Roles.TEACHER.value
    )

@pytest.fixture
def student_user(db):
    return CustomUser.objects.create_user(
        email="student@example.com",
        password="password123",
        first_name="Student",
        last_name="Example",
        role=CustomUser.Roles.STUDENT.value
    )

@pytest.fixture
def course(db, teacher_user):
    return Course.objects.create(
        title="Math 101",
        description="Basic math course",
        lead=teacher_user
    )

def test_course_list(api_client: APIClient, teacher_user, course):
    api_client.force_authenticate(user=teacher_user)
    url = reverse("course-list")
    response = api_client.get(url)

    assert response.status_code == 200

def test_course_retrieve(api_client: APIClient, teacher_user, course):
    api_client.force_authenticate(user=teacher_user)
    url = reverse("course-detail", args=[course.id])
    response = api_client.get(url)

    assert response.status_code == 200

def test_course_create(api_client: APIClient, teacher_user, student_user):
    api_client.force_authenticate(user=teacher_user)
    url = reverse("course-list")

    payload = {
        "title": "Physics 101",
        "description": "Basic physics",
        "lead": teacher_user.id,
        "students": [student_user.id],
        "teachers": []
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201

def test_course_update(api_client: APIClient, teacher_user, course):
    api_client.force_authenticate(user=teacher_user)
    url = reverse("course-detail", args=[course.id])

    payload = {
        "title": "Updated Math 101",
        "description": "Updated description",
        "lead": teacher_user.id,
        "students": [],
        "teachers": []
    }

    response = api_client.put(url, payload, format="json")

    assert response.status_code == 200

def test_course_partial_update(api_client: APIClient, teacher_user, course):
    api_client.force_authenticate(user=teacher_user)
    url = reverse("course-detail", args=[course.id])

    payload = {
        "description": "Partially updated description"
    }

    response = api_client.patch(url, payload, format="json")

    assert response.status_code == 200

def test_course_delete(api_client: APIClient, teacher_user, course):
    api_client.force_authenticate(user=teacher_user)
    url = reverse("course-detail", args=[course.id])

    response = api_client.delete(url)

    assert response.status_code == 204

def test_student_cannot_delete_course(api_client: APIClient, student_user: CustomUser, course: Course):
    api_client.force_authenticate(user=student_user)
    url = reverse("course-detail", args=[course.id])

    response = api_client.delete(url)

    assert response.status_code == 403

def test_non_lead_teacher_cannot_delete_course(api_client: APIClient, teacher_user: CustomUser, course: Course):
    other_teacher = CustomUser.objects.create_user(
        email="other_teacher@example.com",
        password="password123",
        first_name="Other",
        last_name="Teacher",
        role=CustomUser.Roles.TEACHER.value
    )

    api_client.force_authenticate(user=other_teacher)
    url = reverse("course-detail", args=[course.id])
    response = api_client.delete(url)

    assert response.status_code == 403
