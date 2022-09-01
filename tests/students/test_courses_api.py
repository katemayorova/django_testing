import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=1)
    id = courses[0].id

    response = client.get(f'/api/v1/courses/{id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == id


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=5)

    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_filter_id(client, course_factory):
    courses = course_factory(_quantity=5)

    response = client.get('/api/v1/courses/3/')
    assert response.status_code == 200
    course = response.json()
    assert course['id'] == courses[2].id


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    courses = course_factory(_quantity=3)

    response = client.get(f'/api/v1/courses/?name={courses[2].name}')
    assert response.status_code == 200
    course = response.json()
    assert course[0]['name'] == courses[2].name


@pytest.mark.django_db
def test_create_course(client):

    response = client.post('/api/v1/courses/', data={'id': 4, 'name': 'FFFF'})
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=3)
    course_id = courses[2].id

    new_name = 'AAASS'
    response = client.put(f'/api/v1/courses/{course_id}/', {'name': new_name})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == new_name


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=3)
    course_id = courses[1].id

    response = client.delete(f'/api/v1/courses/{course_id}/')
    assert response.status_code == 204
    courses_get = client.get(f'/api/v1/courses/{course_id}/')
    assert courses_get.status_code == 404
