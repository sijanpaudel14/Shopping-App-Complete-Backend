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
    ordering_fields = ['unit_price', 'last_update']

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

        # ✅ Optimized: Prefetch all related data to avoid N+1 queries
        base_queryset = Order.objects.select_related('customer__user') \
            .prefetch_related(
                'items__product__collection',
                'items__product__images'
        )

        if user.is_staff:
            return base_queryset.all()

        # ✅ Optimized: Use values_list to get only the customer ID
        customer_id = Customer.objects.filter(
            user_id=user.id
        ).values_list('id', flat=True).first()

        if customer_id:
            return base_queryset.filter(customer_id=customer_id)

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
