import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from domain.models import Submission, CustomUser, Homework

def test_student_can_create_submission(api_client: APIClient, student_user: CustomUser, homework: Homework):
    homework.lecture.course.students.add(student_user)
    api_client.force_authenticate(user=student_user)
    url = reverse("submission-list")

    data = {
        "content": "My solution",
        "homework": homework.id
    }

    response = api_client.post(url, data, format='json')
    print(response.data)
    
    assert response.status_code == 201

    assert Submission.objects.get(content=data['content']).author == student_user

def test_teacher_can_see_submissions_for_their_lecture(api_client: APIClient, submission: Submission):
    lecture = submission.homework.lecture

    api_client.force_authenticate(user=lecture.teacher)
    url = reverse("submission-list")
    response = api_client.get(url, {"lecture": lecture.id})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == submission.id


def test_student_cannot_see_submissions_for_unenrolled_lecture(api_client: APIClient, submission: Submission):
    other_student = CustomUser.objects.create(
        email="new@example.com",
        password="password123",
        first_name="StudentNEw",
        last_name="ExampleNew",
        role=CustomUser.Roles.STUDENT.value
    )

    api_client.force_authenticate(user=other_student)
    url = reverse("submission-list")
    response = api_client.get(url, {"lecture": submission.homework.lecture.id})

    assert response.status_code == 200
    assert len(response.data) == 0

def test_student_cannot_update_others_submission(api_client: APIClient, submission: Submission):
    other_student = CustomUser.objects.create(
        email="new@example.com",
        password="password123",
        first_name="StudentNEw",
        last_name="ExampleNew",
        role=CustomUser.Roles.STUDENT.value
    )

    api_client.force_authenticate(user=other_student)
    url = reverse("submission-detail", args=[submission.id])
    response = api_client.patch(url, {"content": "Hacked!"})

    assert response.status_code in (404, 403)
