import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from domain.models import CustomUser, Course

def test_student_cannot_delete_course(api_client: APIClient, student_user: CustomUser, teacher_user: CustomUser):
    course = Course.objects.create(
        title="Enrolled Course",
        lead=teacher_user
    )
    course.students.add(student_user)

    api_client.force_authenticate(user=student_user)
    url = reverse("course-detail", args=[course.id])
    response = api_client.delete(url)
    assert response.status_code == 403

def test_teacher_sees_only_lead_courses(api_client: APIClient, teacher_user: CustomUser):
    lead_course = Course.objects.create(title="Lead Course", lead=teacher_user)

    teaching_course = Course.objects.create(
        title="Teaching Course",
        lead=CustomUser.objects.create_user(
            email="other_lead@test.com",
            password="pass123",
            first_name="Other",
            last_name="Lead",
            role=CustomUser.Roles.TEACHER.value
        )
    )
    teaching_course.teachers.add(teacher_user)

    api_client.force_authenticate(user=teacher_user)
    url = reverse("course-list") + "?view=lead"
    response = api_client.get(url)

    titles = [c["title"] for c in response.data]
    assert titles == ["Lead Course"]

def test_teacher_sees_only_teaching_courses(api_client: APIClient, teacher_user: CustomUser):
    lead_course = Course.objects.create(title="Lead Course", lead=teacher_user)

    teaching_course = Course.objects.create(
        title="Teaching Course",
        lead=CustomUser.objects.create_user(
            email="other_lead@test.com",
            password="pass123",
            first_name="Other",
            last_name="Lead",
            role=CustomUser.Roles.TEACHER.value
        )
    )
    teaching_course.teachers.add(teacher_user)

    api_client.force_authenticate(user=teacher_user)
    url = reverse("course-list") + "?view=teaching"
    response = api_client.get(url)

    titles = [c["title"] for c in response.data]
    assert titles == ["Teaching Course"]

def test_teacher_sees_both_courses_by_default(api_client: APIClient, teacher_user: CustomUser):
    lead_course = Course.objects.create(title="Lead Course", lead=teacher_user)

    teaching_course = Course.objects.create(
        title="Teaching Course",
        lead=CustomUser.objects.create_user(
            email="other_lead@test.com",
            password="pass123",
            first_name="Other",
            last_name="Lead",
            role=CustomUser.Roles.TEACHER.value
        )
    )
    teaching_course.teachers.add(teacher_user)

    api_client.force_authenticate(user=teacher_user)
    url = reverse("course-list")
    response = api_client.get(url)

    titles = [c["title"] for c in response.data]
    assert set(titles) == {"Lead Course", "Teaching Course"}

def test_student_sees_only_enrolled_courses(api_client: APIClient, student_user: CustomUser, teacher_user: CustomUser):
    enrolled_course = Course.objects.create(
        title="Enrolled Course",
        lead=teacher_user
    )
    enrolled_course.students.add(student_user)

    other_course = Course.objects.create(title="Other Course", lead=teacher_user)

    api_client.force_authenticate(user=student_user)
    url = reverse("course-list")
    response = api_client.get(url)

    titles = [c["title"] for c in response.data]
    assert titles == ["Enrolled Course"]

def test_student_sees_all_courses_with_query_param(api_client: APIClient, student_user: CustomUser, teacher_user: CustomUser):
    enrolled_course = Course.objects.create(
        title="Enrolled Course",
        lead=teacher_user
    )
    enrolled_course.students.add(student_user)

    other_course = Course.objects.create(title="Other Course", lead=teacher_user)

    api_client.force_authenticate(user=student_user)
    url = reverse("course-list") + "?all=true"
    response = api_client.get(url)

    titles = [c["title"] for c in response.data]
    assert set(titles) == {"Enrolled Course", "Other Course"}
