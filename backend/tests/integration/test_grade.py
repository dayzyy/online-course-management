import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from domain.models import Grade, CustomUser

def test_teacher_can_create_grade(api_client: APIClient, teacher_user: CustomUser, homework):
    api_client.force_authenticate(user=teacher_user)
    url = reverse("grade-list")

    data = {
        "value": 95,
        "homework": homework.id
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert Grade.objects.filter(id=response.data["id"]).exists()
    assert response.data["value"] == data["value"]
    assert response.data["homework"] == data["homework"]

def test_student_can_view_grades_for_their_course(api_client: APIClient, student_user: CustomUser, grade: Grade):
    grade.homework.lecture.course.students.add(student_user)
    api_client.force_authenticate(user=student_user)
    url = reverse("grade-list")

    response = api_client.get(url)
    assert response.status_code == 200
    assert any(g["id"] == grade.id for g in response.data)

def test_student_cannot_update_or_delete_grade(api_client: APIClient, student_user: CustomUser, grade: Grade):
    api_client.force_authenticate(user=student_user)
    url = reverse("grade-detail", args=[grade.id])

    response = api_client.patch(url, {"value": 100}, format="json")
    assert response.status_code == 403

    response = api_client.delete(url)
    assert response.status_code == 403

def test_teacher_can_filter_grades_by_course(api_client: APIClient, grade: Grade):
    course = grade.homework.lecture.course
    api_client.force_authenticate(user=grade.grader)
    url = reverse("grade-list") + f"?course={course.id}"

    response = api_client.get(url)
    print(response.data)
    assert response.status_code == 200
    assert all(g["homework"]["id"] == grade.homework.id for g in response.data)
