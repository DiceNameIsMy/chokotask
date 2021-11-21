from typing import Optional

import pytest

from rest_framework.test import APIClient

from django.urls import reverse


REFRESH_TOKEN_URL = reverse('refresh-token')

DEFAULT_VALUES = {
    'username': 'test1',
    'password': 'password1',
}


def refresh_token(api_client: APIClient, token_key: str = ''):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token_key}')

    return api_client.post(path=REFRESH_TOKEN_URL)


@pytest.mark.django_db
def test_refresh_token(api_client: APIClient, create_user, create_token):
    user = create_user(DEFAULT_VALUES)
    token = create_token(user)

    request = refresh_token(api_client=api_client, token_key=token.key)

    assert request.status_code == 201


@pytest.mark.django_db
def test_refresh_token_not_valid(api_client: APIClient):
    request = refresh_token(api_client=api_client, token_key='a' * 40)

    assert request.status_code == 401