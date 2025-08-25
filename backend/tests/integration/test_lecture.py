import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from rest_framework.test import APIClient
from domain.models import CustomUser, Lecture, Course

def test_teacher_can_create_lecture(api_client: APIClient,  teacher_user: CustomUser, course: Course):
    api_client.force_authenticate(user=teacher_user)
    url = reverse("lecture-list")

    data = {
        "topic": "New Lecture",
        "teacher": teacher_user.id,
        "presentation": SimpleUploadedFile(
            name="dummy.pdf",
            content=b"Dummy content",
            content_type="application/pdf"
        ),
        "course": course.id,
        "held_at": timezone.now()
    }

    response = api_client.post(url, data, format='multipart')
    assert response.status_code == 201

    lecture = Lecture.objects.get(topic="New Lecture")
    assert lecture.course == course
    assert lecture.teacher == teacher_user
    assert response.data["topic"] == data["topic"]
    assert response.data["course"] == data["course"]

def test_student_can_list_their_lectures(api_client: APIClient, student_user: CustomUser, lecture: Lecture):
    lecture.course.students.add(student_user)

    api_client.force_authenticate(user=student_user)
    url = reverse("lecture-list")
    response = api_client.get(url)

    assert response.status_code == 200

    lecture_ids = [l["id"] for l in response.data]
    assert lecture_ids == [lecture.id]

def test_student_cannot_modify_lecture(api_client: APIClient, student_user: CustomUser, lecture: Lecture):
    api_client.force_authenticate(user=student_user)
    url = reverse("lecture-detail", args=[lecture.id])
    response = api_client.delete(url)

    assert response.status_code == 403

def test_teacher_can_modify_their_lecture(api_client: APIClient, lecture: Lecture):
    api_client.force_authenticate(user=lecture.teacher)
    url = reverse("lecture-detail", args=[lecture.id])
    response = api_client.patch(url, {"topic": "Updated Lecture"}, format="json")

    assert response.status_code == 200

    lecture.refresh_from_db()
    assert lecture.topic == "Updated Lecture"

def test_teacher_cannot_modify_other_teacher_lecture(api_client: APIClient, lecture: Lecture):
    other_teacher = CustomUser.objects.create_user(
        email="other_teacher@test.com",
        password="password123",
        first_name="Other",
        last_name="Teacher",
        role=CustomUser.Roles.TEACHER.value
    )

    api_client.force_authenticate(user=other_teacher)
    url = reverse("lecture-detail", args=[lecture.id])
    response = api_client.patch(url, {"topic": "Hacked Lecture"}, format="json")

    assert response.status_code in (403, 404)
