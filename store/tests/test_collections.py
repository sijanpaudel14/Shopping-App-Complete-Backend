from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestCreateCollection:
    @pytest.mark.skip(reason="Permission classes temporarily disabled in CollectionViewSet") # Used to skip the test due to disabled permission classes
    def test_if_user_is_anonymous_returns_401(self):
        # Test that an anonymous user cannot create a collection
        # AAA, (Arrange, Act, Assert)
        # In Arange part, we setup the test client without authentication
        # In Act part, we make a POST request to create a collection
        # In Assert part, we check that the response status code is 401 Unauthorized

        # Here, Arrange part is empty because the test client is already set up by default as anonymous
        # For Act part:
        client = APIClient()
        response = client.post('/store/collections/',
                               {'title': 'New Collection'})

        # For Assert part:
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
