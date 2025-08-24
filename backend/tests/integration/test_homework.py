import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from domain.models import CustomUser, Course, Lecture, Homework


def test_student_can_list_their_homeworks(api_client: APIClient, student_user: CustomUser, teacher_user: CustomUser):
    course = Course.objects.create(title="Test Course", lead=teacher_user)
    course.students.add(student_user)

    lecture = Lecture.objects.create(
        topic="Lecture 1",
        course=course,
        teacher=teacher_user,
        held_at=timezone.now()
    )
    Homework.objects.create(
        content="Homework 1",
        lecture=lecture,
        due=timezone.now() + timezone.timedelta(days=7)
    )

    api_client.force_authenticate(user=student_user)
    url = reverse("homework-list")
    response = api_client.get(url)

    assert response.status_code == 200

    contents = [h["content"] for h in response.data]
    assert "Homework 1" in contents

def test_student_cannot_modify_homework(api_client: APIClient, student_user: CustomUser, teacher_user: CustomUser):
    course = Course.objects.create(title="Test Course", lead=teacher_user)
    lecture = Lecture.objects.create(
        topic="Lecture 1",
        course=course,
        teacher=teacher_user,
        held_at=timezone.now()
    )
    homework = Homework.objects.create(
        content="Homework 1",
        lecture=lecture,
        due=timezone.now() + timezone.timedelta(days=7)
    )

    api_client.force_authenticate(user=student_user)
    url = reverse("homework-detail", args=[homework.id])
    response = api_client.delete(url)

    assert response.status_code == 403

def test_teacher_can_modify_their_homework(api_client: APIClient, teacher_user: CustomUser):
    course = Course.objects.create(title="Test Course", lead=teacher_user)
    lecture = Lecture.objects.create(
        topic="Lecture 1",
        course=course,
        teacher=teacher_user,
        held_at=timezone.now()
    )
    homework = Homework.objects.create(
        content="Homework 1",
        lecture=lecture,
        due=timezone.now() + timezone.timedelta(days=7)
    )

    api_client.force_authenticate(user=teacher_user)
    url = reverse("homework-detail", args=[homework.id])
    response = api_client.patch(url, {"content": "Updated Homework"}, format="json")

    assert response.status_code == 200

    homework.refresh_from_db()
    assert homework.content == "Updated Homework"

def test_teacher_cannot_modify_other_teacher_homework(api_client: APIClient, teacher_user: CustomUser):
    other_teacher = CustomUser.objects.create_user(
        email="other_teacher@test.com",
        password="password123",
        first_name="Other",
        last_name="Teacher",
        role=CustomUser.Roles.TEACHER.value
    )

    course = Course.objects.create(title="Other Course", lead=other_teacher)
    lecture = Lecture.objects.create(
        topic="Other Lecture",
        course=course,
        teacher=other_teacher,
        held_at=timezone.now()
    )
    homework = Homework.objects.create(
        content="Other Homework",
        lecture=lecture,
        due=timezone.now() + timezone.timedelta(days=7)
    )

    api_client.force_authenticate(user=teacher_user)
    url = reverse("homework-detail", args=[homework.id])
    response = api_client.patch(url, {"content": "Hacked Homework"}, format="json")

    assert response.status_code in (403, 404)
