import pytest
from tests.factories import AdFactory


@pytest.mark.django_db
def test_create_selection(client, users, user_token):
    ad_list = AdFactory.create_batch(3)

    expected_response = {
        "id": 1,
        "name": "test selection",
        "owner": users.username,
        "items": [ad.pk for ad in ad_list]
    }

    data = {
        "name": "test selection",
        "owner": users.username,
        "items": [ad.pk for ad in ad_list],
    }

    response = client.post(
        "/selection/",
        data,
        HTTP_AUTHORIZATION="Bearer " + user_token,
        content_type="application/json",

    )

    assert response.status_code == 201
    assert response.data == expected_response
