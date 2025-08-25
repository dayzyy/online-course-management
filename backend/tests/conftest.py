import pytest
from domain.models import CustomUser, Course, Lecture, Homework, Submission, Grade
from rest_framework.test import APIClient
from django.utils import timezone

_DEFAULT_USER_PASSWORD = 'password123'

@pytest.fixture
def default_user(db) -> CustomUser:
    return CustomUser.objects.create_user(
        email='luka@gmail.com',
        password=_DEFAULT_USER_PASSWORD,
        first_name='Luka',
        last_name='Mania',
        role=CustomUser.Roles.STUDENT.value
    )

@pytest.fixture
def default_user_password() -> str:
    return _DEFAULT_USER_PASSWORD

@pytest.fixture()
def api_client() -> APIClient:
    return APIClient()

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
def course(teacher_user: CustomUser):
    return Course.objects.create(
        title="Premade course",
        lead=teacher_user
    )

@pytest.fixture
def lecture(teacher_user: CustomUser, course: Course):
    return Lecture.objects.create(
        topic="Lecture 1",
        course=course,
        teacher=teacher_user,
        held_at=timezone.now()
    )

@pytest.fixture
def homework(lecture: Lecture):
    return Homework.objects.create(
        content="Homework 1",
        lecture=lecture,
        due=timezone.now() + timezone.timedelta(days=7)
    )

@pytest.fixture
def submission(homework: Homework, student_user: CustomUser):
    return Submission.objects.create(
        content="Answer 1",
        homework=homework,
        author=student_user
    )

@pytest.fixture
def grade(homework: Homework):
    return Grade.objects.create(
        value=100,
        homework=homework,
        grader=homework.lecture.teacher
    )
