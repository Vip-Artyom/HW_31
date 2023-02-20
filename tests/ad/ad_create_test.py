import pytest


@pytest.mark.django_db
def test_create_ad(client, users, category, user_token):
    data = {
        "name": "name name name",
        "price": 18000,
        "author": users.pk,
        "category": category.pk
    }

    expected_response = {
        "id": 1,
        "is_published": False,
        "name": "name name name",
        "price": 18000,
        "description": None,
        "image": None,
        "author": users.pk,
        "category": category.pk,
    }

    response = client.post(
        "/ad/",
        data,
        HTTP_AUTHORIZATION="Bearer " + user_token
    )

    assert response.status_code == 201
    assert response.data == expected_response
