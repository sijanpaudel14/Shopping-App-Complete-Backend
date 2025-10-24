from rest_framework import status
import pytest


@pytest.fixture
def create_collection(api_client):
    def _create_collection(collection_data):
        return api_client.post('/store/collections/', collection_data)
    return _create_collection


@pytest.mark.django_db
class TestCreateCollection:
    # Used to skip the test due to disabled permission classes
    # @pytest.mark.skip(reason="Permission classes temporarily disabled in CollectionViewSet")
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        # Test that an anonymous user cannot create a collection
        # AAA, (Arrange, Act, Assert)
        # Here, Arrange part is empty because the test client is already set up by default as anonymous

        # In Arrange part, we setup the test client without authentication

        # In Act part, we make a POST request to create a collection
        # For Act part:
        response = create_collection({
            'title': 'a'
        })

        # In Assert part, we check that the response status code is 401 Unauthorized
        # For Assert part:
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_collection):
        # force_authenticate method is used to simulate an authenticated user who is not an admin
        authenticate(is_staff=False)

        response = create_collection({
            'title': 'a'
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_collection):
        authenticate(is_staff=True)

        response = create_collection({
            'title': ''  # Invalid data: title is required to be non-empty
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    # Enhanced test case to check for valid data
    def test_if_data_is_valid_returns_201(self, authenticate, create_collection):
        authenticate(is_staff=True)

        response = create_collection({
            'title': 'Valid Collection Title'
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
