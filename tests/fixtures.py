import pytest


@pytest.fixture
@pytest.mark.django_db
def user_token(client, django_user_model):
    username = "username"
    password = "password"

    django_user_model.objects.create(
        username=username,
        password=password,
        role="moderator"
    )

    response = client.post("/user/token/", {"username": username, "password": password})

    return response.data.get("access")
