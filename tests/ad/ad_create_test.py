import pytest


@pytest.mark.django_db
def test_create_ad(client, user, category, user_token):
    expected_response = {
        "id": 1,
        "category": category.pk,
        "is_published": False,
        "name": 'name name name',
        "price": 18000,
        "description": None,
        "author": user.id,
    }

    data = {
        "name": 'name name name',
        "price": 18000,
        "author": user.id,
        "category": category.pk
    }

    response = client.post(
        '/ad/create/',
        data,
        HTTP_AUTHORIZATION="Bearer " + user_token,
        content_type='application/json'
    )

    assert response.status_code == 201
    assert response.data == expected_response
