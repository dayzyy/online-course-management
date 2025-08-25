import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from domain.models import CustomUser, Homework, Lecture

def test_teacher_can_create_homework(api_client: APIClient, lecture: Lecture):
    api_client.force_authenticate(user=lecture.teacher)
    url = reverse("homework-list")

    data = {
        "content": "New Homework",
        "lecture": lecture.id,
        "due": (timezone.now() + timedelta(days=7)).isoformat()
    }

    response = api_client.post(url, data, format='json')

    print(response.status_code)
    print(response.data)

    assert response.status_code == 201

    homework = Homework.objects.get(content="New Homework")
    assert homework.lecture == lecture
    assert response.data["content"] == data["content"]
    assert response.data["lecture"] == data["lecture"]

def test_student_can_list_their_homeworks(api_client: APIClient, student_user: CustomUser, homework: Homework):
    homework.lecture.course.students.add(student_user)

    api_client.force_authenticate(user=student_user)
    url = reverse("homework-list")
    response = api_client.get(url)

    assert response.status_code == 200

    hw_ids = [h["id"] for h in response.data]
    assert hw_ids == [homework.id]

def test_student_cannot_modify_homework(api_client: APIClient, student_user: CustomUser, homework: Homework):
    api_client.force_authenticate(user=student_user)
    url = reverse("homework-detail", args=[homework.id])
    response = api_client.delete(url)

    assert response.status_code == 403

def test_teacher_can_modify_their_homework(api_client: APIClient, homework: Homework):
    api_client.force_authenticate(user=homework.lecture.teacher)
    url = reverse("homework-detail", args=[homework.id])
    response = api_client.patch(url, {"content": "Updated Homework"}, format="json")

    assert response.status_code == 200

    homework.refresh_from_db()
    assert homework.content == "Updated Homework"

def test_teacher_cannot_modify_other_teacher_homework(api_client: APIClient, homework: Homework):
    other_teacher = CustomUser.objects.create_user(
        email="other_teacher@test.com",
        password="password123",
        first_name="Other",
        last_name="Teacher",
        role=CustomUser.Roles.TEACHER.value
    )

    api_client.force_authenticate(user=other_teacher)
    url = reverse("homework-detail", args=[homework.id])
    response = api_client.patch(url, {"content": "Hacked Homework"}, format="json")

    assert response.status_code in (403, 404)

def test_teacher_can_filter_homework_by_lecture(api_client: APIClient, homework: Homework):
    api_client.force_authenticate(user=homework.lecture.teacher)
    url = reverse("homework-list")
    response = api_client.get(url, {"lecture": homework.lecture.id})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == homework.id

def test_student_cannot_filter_homework_for_unenrolled_lecture(api_client, student_user, homework: Homework):
    api_client.force_authenticate(user=student_user)
    url = reverse("homework-list")
    response = api_client.get(url, {"lecture": homework.lecture.id})

    assert response.status_code == 200
    # student is not enrolled in course -> should see nothing
    assert len(response.data) == 0
