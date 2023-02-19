import pytest
from tests.factories import AdFactory


@pytest.mark.django_db
def test_create_selection(client, user, user_token):
    ad_list = AdFactory.create_batch(3)

    expected_response = {
        "id": 1,
        "name": "test selection",
        "owner": user.username,
        "items": [ad.pk for ad in ad_list]
    }

    data = {
        'name': 'test selection',
        'owner': user.username,
        'items': [ad.pk for ad in ad_list],
    }

    response = client.post(
        '/selection/create/',
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION='Bearer ' + user_token
    )

    assert response.status_code == 201
    assert response.data == expected_response