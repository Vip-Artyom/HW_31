import pytest
from ads.serializers.ad_serializers import AdListSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_list(client, user_token):
    ads = AdFactory.create_batch(3)

    expected_response = {
        "count": 3,
        "next": None,
        "previous": None,
        "results": AdListSerializer(ads, many=True).data
    }

    response = client.get(
        "/ad/",
        HTTP_AUTHORIZATION="Bearer " + user_token
    )

    assert response.status_code == 200
    assert response.data == expected_response
