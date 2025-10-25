# from store.permissions import FullDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermission
# from store.pagination import DefaultPagination
# from django.db.models.aggregates import Count
# from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.decorators import action, permission_classes
# from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
# from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet, GenericViewSet
# from rest_framework import status
# from .filters import ProductFilter
# from .models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product, ProductImage, Review
# from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, CreateOrderSerializer, CustomerSerializer, OrderSerializer, ProductImageSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer, UpdateOrderSerializer


# class ProductViewSet(ModelViewSet):
#     # Remove this line - we'll use get_queryset() instead
#     # queryset = Product.objects.all()

#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_class = ProductFilter
#     pagination_class = DefaultPagination
#     permission_classes = [IsAdminOrReadOnly]
#     search_fields = ['title', 'description']
#     ordering_fields = ['unit_price', 'last_update']

#     def get_queryset(self):
#         # Optimize queries by prefetching images and selecting collection
#         return Product.objects.select_related('collection') \
#                               .prefetch_related('images') \
#                               .all()

#     def get_serializer_context(self):
#         return {'request': self.request}

#     def destroy(self, request, *args, **kwargs):
#         if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
#             return Response(
#                 {'error': 'Product cannot be deleted because it is associated with an order item.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED
#             )
#         return super().destroy(request, *args, **kwargs)


# class CollectionViewSet(ModelViewSet):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')).all()
#     serializer_class = CollectionSerializer
#     permission_classes = [IsAdminOrReadOnly]

#     def destroy(self, request, *args, **kwargs):
#         if Product.objects.filter(collection_id=kwargs['pk']):
#             return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

#         return super().destroy(request, *args, **kwargs)


# class ReviewViewSet(ModelViewSet):
#     serializer_class = ReviewSerializer

#     def get_queryset(self):
#         return Review.objects.filter(product_id=self.kwargs['product_pk'])

#     def get_serializer_context(self):
#         return {'product_id': self.kwargs['product_pk']}


# class CartViewSet(CreateModelMixin,
#                   RetrieveModelMixin,
#                   DestroyModelMixin,
#                   GenericViewSet):
#     queryset = Cart.objects.prefetch_related('items__product').all()
#     serializer_class = CartSerializer


# class CartItemViewSet(ModelViewSet):
#     http_method_names = ['get', 'post', 'patch', 'delete']

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return AddCartItemSerializer
#         elif self.request.method == 'PATCH':
#             return UpdateCartItemSerializer
#         return CartItemSerializer

#     def get_serializer_context(self):
#         return {'cart_id': self.kwargs['cart_pk']}

#     def get_queryset(self):
#         return CartItem.objects \
#             .filter(cart_id=self.kwargs['cart_pk']) \
#             .select_related('product')


# class CustomerViewSet(ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#     permission_classes = [IsAdminUser]

#     @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
#     def history(self, request, pk):
#         return Response('ok')

#     @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
#     def me(self, request):
#         customer = Customer.objects.get(
#             user_id=request.user.id)
#         if request.method == 'GET':
#             serializer = CustomerSerializer(customer)
#             return Response(serializer.data)
#         elif request.method == 'PUT':
#             serializer = CustomerSerializer(customer, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)


# class OrderViewSet(ModelViewSet):
#     http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

#     def get_permissions(self):
#         if self.request.method in ['PATCH', 'DELETE']:
#             return [IsAdminUser()]
#         return [IsAuthenticated()]

#     def create(self, request, *args, **kwargs):
#         serializer = CreateOrderSerializer(
#             data=request.data,
#             context={'user_id': self.request.user.id})
#         serializer.is_valid(raise_exception=True)
#         order = serializer.save()
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return CreateOrderSerializer
#         elif self.request.method == 'PATCH':
#             return UpdateOrderSerializer
#         return OrderSerializer

#     def get_queryset(self):
#         user = self.request.user

#         if user.is_staff:
#             return Order.objects.all()

#         customer_id = Customer.objects.only(
#             'id').get(user_id=user.id)
#         return Order.objects.filter(customer_id=customer_id)


# class ProductImageViewSet(ModelViewSet):
#     serializer_class = ProductImageSerializer

#     def get_serializer_context(self):
#         return {
#             'product_id': self.kwargs['product_pk']
#         }

#     def get_queryset(self):
#         return ProductImage.objects.select_related('product').filter(product_id=self.kwargs['product_pk'])


from rest_framework.decorators import api_view, permission_classes
import sys
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model  # ✅ Use this
from rest_framework.permissions import AllowAny
import os
from django.conf import settings
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from store.permissions import FullDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermission
from store.pagination import DefaultPagination
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from .filters import ProductFilter
from .models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product, ProductImage, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, CreateOrderSerializer, CustomerSerializer, OrderSerializer, ProductImageSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer, UpdateOrderSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update', 'title']

    def get_queryset(self):
        # ✅ Optimized with select_related and prefetch_related
        queryset = Product.objects.select_related('collection') \
                                  .prefetch_related('images')

        # ✅ Only fetch necessary fields for list views
        if self.action == 'list':
            queryset = queryset.only(
                'id', 'title', 'slug', 'description',
                'unit_price', 'inventory', 'collection_id', 'collection__title'
            )

        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        # ✅ Use exists() instead of count() - much faster
        if OrderItem.objects.filter(product_id=kwargs['pk']).exists():
            return Response(
                {'error': 'Product cannot be deleted because it is associated with an order item.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        # ✅ Optimized: Use annotate with Count for products_count
        return Collection.objects.annotate(
            products_count=Count('products')
        ).all()

    def destroy(self, request, *args, **kwargs):
        # ✅ Use exists() instead of boolean filter check
        if Product.objects.filter(collection_id=kwargs['pk']).exists():
            return Response(
                {'error': 'Collection cannot be deleted because it includes one or more products.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # ✅ Select related product to avoid N+1 queries
        return Review.objects.filter(
            product_id=self.kwargs['product_pk']
        ).select_related('product')

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        # ✅ Optimized: Prefetch cart items with products, collections, and images
        return Cart.objects.prefetch_related(
            'items__product__collection',
            'items__product__images'
        ).all()


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        # ✅ Optimized: Select related and prefetch related data
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product__collection') \
            .prefetch_related('product__images')


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # ✅ Optimized: Select related user to avoid extra queries
        return Customer.objects.select_related('user').all()

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # ✅ Optimized: Select related user
        customer = Customer.objects.select_related('user').get(
            user_id=request.user.id
        )

        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        # ✅ Debug prints
        print(f"=== GET ORDERS REQUEST ===")
        print(f"User: {user}")
        print(f"User ID: {user.id}")
        print(f"User email: {user.email}")
        print(f"Is staff: {user.is_staff}")

        # Optimized: Prefetch all related data to avoid N+1 queries
        base_queryset = Order.objects.select_related('customer__user') \
            .prefetch_related(
                'items__product__collection',
                'items__product__images'
        )

        if user.is_staff:
            print("User is staff - returning all orders")
            return base_queryset.all()

        # Optimized: Use values_list to get only the customer ID
        customer_id = Customer.objects.filter(
            user_id=user.id
        ).values_list('id', flat=True).first()

        # ✅ Debug prints
        print(f"Customer ID found: {customer_id}")

        if customer_id:
            orders = base_queryset.filter(customer_id=customer_id)
            print(f"Orders count: {orders.count()}")
            for order in orders:
                print(f"  - Order #{order.id}")
            return orders

        print("No customer found - returning empty queryset")
        return Order.objects.none()


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {
            'product_id': self.kwargs['product_pk']
        }

    def get_queryset(self):
        # ✅ Optimized: Select related product and only fetch needed fields
        return ProductImage.objects.select_related('product').filter(
            product_id=self.kwargs['product_pk']
        ).only('id', 'image', 'product_id')


# inside views.py


class CustomGoogleOAuth2Client(OAuth2Client):
    def __init__(
        self,
        request,
        consumer_key,
        consumer_secret,
        access_token_method,
        access_token_url,
        callback_url,
        _scope,  # This is fix for incompatibility between django-allauth==65.3.1 and dj-rest-auth==7.0.1
        scope_delimiter=" ",
        headers=None,
        basic_auth=False,
    ):
        super().__init__(
            request,
            consumer_key,
            consumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            scope_delimiter,
            headers,
            basic_auth,
        )


# if you want to use Authorization Code Grant, use this
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.environ["GOOGLE_CALLBACK_URL"]
    client_class = CustomGoogleOAuth2Client


User = get_user_model()  # ✅ Get the actual User model


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """Simple Google OAuth"""
    print("=" * 80, file=sys.stderr)
    print("GOOGLE LOGIN CALLED", file=sys.stderr)
    print("=" * 80, file=sys.stderr)

    code = request.data.get('code')
    print(f"Code received: {bool(code)}", file=sys.stderr)

    if not code:
        return Response({'non_field_errors': ['Code required']}, status=400)

    # Get credentials
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')

    print(f"Client ID exists: {bool(client_id)}", file=sys.stderr)
    print(f"Client Secret exists: {bool(client_secret)}", file=sys.stderr)

    if not client_id or not client_secret:
        return Response({
            'non_field_errors': ['OAuth credentials not configured']
        }, status=500)

    try:
        # Exchange code for token
        token_response = requests.post('https://oauth2.googleapis.com/token', data={
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': 'http://localhost:3000/auth/callback/google',
            'grant_type': 'authorization_code',
        })

        print(f"Google status: {token_response.status_code}", file=sys.stderr)

        if token_response.status_code != 200:
            print(f"Google error: {token_response.text}", file=sys.stderr)
            return Response({
                'non_field_errors': ['Failed to exchange code for access token'],
                'details': token_response.json()
            }, status=400)

        tokens = token_response.json()

        # Get user info
        user_response = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            headers={'Authorization': f"Bearer {tokens['access_token']}"}
        )
        user_info = user_response.json()

        print(f"User email: {user_info.get('email')}", file=sys.stderr)

        # Create or get user (using custom User model)
        user, created = User.objects.get_or_create(
            email=user_info['email'],
            defaults={
                'username': user_info['email'].split('@')[0],
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', ''),
            }
        )

        print(
            f"User {'created' if created else 'found'}: {user.email}", file=sys.stderr)

        # Generate JWT
        refresh = RefreshToken.for_user(user)

        print("JWT tokens generated successfully", file=sys.stderr)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return Response({'non_field_errors': [str(e)]}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def github_login(request):
    """Simple GitHub OAuth"""
    print("=" * 80, file=sys.stderr)
    print("GITHUB LOGIN CALLED", file=sys.stderr)
    print("=" * 80, file=sys.stderr)

    code = request.data.get('code')
    print(f"Code received: {bool(code)}", file=sys.stderr)

    if not code:
        return Response({'non_field_errors': ['Code required']}, status=400)

    # Get credentials
    client_id = os.environ.get('GITHUB_CLIENT_ID')
    client_secret = os.environ.get('GITHUB_CLIENT_SECRET')

    print(f"Client ID exists: {bool(client_id)}", file=sys.stderr)
    print(f"Client Secret exists: {bool(client_secret)}", file=sys.stderr)

    if not client_id or not client_secret:
        return Response({
            'non_field_errors': ['OAuth credentials not configured']
        }, status=500)

    try:
        # Exchange code for token
        token_response = requests.post(
            'https://github.com/login/oauth/access_token',
            data={
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'redirect_uri': 'http://localhost:3000/auth/callback/github',
            },
            headers={'Accept': 'application/json'}
        )

        print(
            f"GitHub token status: {token_response.status_code}", file=sys.stderr)

        if token_response.status_code != 200:
            print(f"GitHub error: {token_response.text}", file=sys.stderr)
            return Response({
                'non_field_errors': ['Failed to exchange code for access token'],
                'details': token_response.json()
            }, status=400)

        tokens = token_response.json()

        if 'error' in tokens:
            print(f"GitHub OAuth error: {tokens}", file=sys.stderr)
            return Response({
                'non_field_errors': [tokens.get('error_description', 'OAuth failed')]
            }, status=400)

        access_token = tokens.get('access_token')

        # Get user info
        user_response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        user_info = user_response.json()

        # Get user email (might need separate request)
        email = user_info.get('email')
        if not email:
            email_response = requests.get(
                'https://api.github.com/user/emails',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            emails = email_response.json()
            primary_email = next((e for e in emails if e.get('primary')), None)
            email = primary_email['email'] if primary_email else f"{user_info['login']}@github.local"

        print(f"GitHub user email: {email}", file=sys.stderr)

        # Get name
        name = user_info.get('name', '').split(
            ' ', 1) if user_info.get('name') else ['', '']
        first_name = name[0] if name else user_info.get('login', '')
        last_name = name[1] if len(name) > 1 else ''

        # Create or get user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': user_info.get('login', email.split('@')[0]),
                'first_name': first_name,
                'last_name': last_name,
            }
        )

        print(
            f"User {'created' if created else 'found'}: {user.email}", file=sys.stderr)

        # Generate JWT
        refresh = RefreshToken.for_user(user)

        print("JWT tokens generated successfully", file=sys.stderr)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return Response({'non_field_errors': [str(e)]}, status=500)
