from rest_framework.test import APIClient
from rest_framework import status
import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestCreateCollection:
    # Used to skip the test due to disabled permission classes
    # @pytest.mark.skip(reason="Permission classes temporarily disabled in CollectionViewSet")
    def test_if_user_is_anonymous_returns_401(self):
        # Test that an anonymous user cannot create a collection
        # AAA, (Arrange, Act, Assert)
        # Here, Arrange part is empty because the test client is already set up by default as anonymous

        # In Arrange part, we setup the test client without authentication
        client = APIClient()
        

        # In Act part, we make a POST request to create a collection
        # For Act part:
        response = client.post('/store/collections/',
                               {'title': 'New Collection'})

        # In Assert part, we check that the response status code is 401 Unauthorized
        client = APIClient()
        response = client.post('/store/collections/',
                               {'title': 'New Collection'})

        # For Assert part:
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_user_is_not_admin_returns_403(self):
        client = APIClient()
        # force_authenticate method is used to simulate an authenticated user who is not an admin   
        client.force_authenticate(user={})

        response = client.post('/store/collections/',{
            'title':'a'
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN

