import pytest
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def _authenticate(is_staff=False):
        # force_authenticate method is used to simulate an authenticated user who is not an admin
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return _authenticate
