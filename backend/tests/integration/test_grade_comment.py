import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from domain.models import CustomUser, GradeComment, Grade

@pytest.fixture
def comment_by_student(student_user: CustomUser, grade: Grade) -> GradeComment:
    return GradeComment.objects.create(
        content="My comment",
        author=student_user,
        grade=grade,
    )

@pytest.fixture
def comment_by_teacher(teacher_user, grade: Grade) -> GradeComment:
    return GradeComment.objects.create(
        content="Teacher feedback",
        author=teacher_user,
        grade=grade,
    )

def test_list_only_shows_own_comments(api_client: APIClient, student_user: CustomUser, comment_by_student: GradeComment, comment_by_teacher: GradeComment):
    api_client.force_authenticate(student_user)
    url = reverse("grade_comment-list")

    response = api_client.get(url)
    assert response.status_code == 200

    ids = [c["id"] for c in response.json()]
    assert comment_by_student.id in ids
    assert comment_by_teacher.id not in ids

def test_retrieve_other_comment_forbidden(api_client: APIClient, student_user: CustomUser, comment_by_teacher: GradeComment):
    api_client.force_authenticate(student_user)
    url = reverse("grade_comment-detail", args=[comment_by_teacher.id])

    response = api_client.get(url)
    assert response.status_code in (404, 403)
