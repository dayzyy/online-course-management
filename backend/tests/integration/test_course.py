import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from domain.models import CustomUser, Course

def test_teacher_can_create_course(api_client: APIClient, teacher_user: CustomUser):
    api_client.force_authenticate(user=teacher_user)
    url = reverse("course-list")

    data = {
        "title": "New Course",
        "description": "Course description",
        "teachers": [],
        "students": []
    }

    response = api_client.post(url, data, format='json')
    
    assert response.status_code == 201
    assert Course.objects.filter(title=data["title"], lead=teacher_user).exists()
    assert response.data["title"] == "New Course"
    assert response.data["lead"]["id"] == teacher_user.id

def test_student_cannot_delete_course(api_client: APIClient, student_user: CustomUser, course: Course):
    course.students.add(student_user)

    api_client.force_authenticate(user=student_user)
    url = reverse("course-detail", args=[course.id])
    response = api_client.delete(url)

    assert response.status_code == 403

def test_teacher_sees_only_lead_courses(api_client: APIClient, teacher_user: CustomUser, course: Course):
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

    course_ids = [c["id"] for c in response.data]
    assert course_ids == [course.id]

def test_teacher_sees_only_teaching_courses(api_client: APIClient, teacher_user: CustomUser):
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

    course_ids = [c["id"] for c in response.data]
    assert course_ids == [teaching_course.id]

def test_teacher_sees_both_courses_by_default(api_client: APIClient, teacher_user: CustomUser, course: Course):
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

    course_ids = [c["id"] for c in response.data]
    assert set(course_ids) == {course.id, teaching_course.id}

def test_student_sees_only_enrolled_courses(api_client: APIClient, student_user: CustomUser, teacher_user: CustomUser, course: Course):
    enrolled_course = Course.objects.create(
        title="Enrolled Course",
        lead=teacher_user
    )
    enrolled_course.students.add(student_user)

    api_client.force_authenticate(user=student_user)
    url = reverse("course-list")
    response = api_client.get(url)

    course_ids = [c["id"] for c in response.data]
    assert course_ids == [enrolled_course.id]
