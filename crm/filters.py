# crm/filters.py

import django_filters
from .models import Customer, Product, Order
from django.db.models import Q
from decimal import Decimal

# Custom filter method for phone pattern
def filter_phone_pattern(queryset, name, value):
    return queryset.filter(phone__startswith=value)

# Custom filter method for product name in order
def filter_by_product_name(queryset, name, value):
    if value:
        return queryset.filter(products__name__icontains=value).distinct()
    return queryset

# Custom filter method for product ID in order
def filter_by_product_id(queryset, name, value):
    if value:
        return queryset.filter(products__id__exact=value).distinct()
    return queryset


# --- CustomerFilter ---
class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    
    created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    # Challenge: Custom filter
    phone_pattern = django_filters.CharFilter(method=filter_phone_pattern)

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'created_at']


# --- ProductFilter ---
class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    stock__gte = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock__lte = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']


# --- OrderFilter ---
class OrderFilter(django_filters.FilterSet):
    total_amount__gte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount__lte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    
    order_date__gte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='gte')
    order_date__lte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='lte')
    
    # Challenge: Filtering by related model field
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    product_name = django_filters.CharFilter(method=filter_by_product_name)
    product_id = django_filters.CharFilter(method=filter_by_product_id)

    class Meta:
        model = Order
        fields = ['total_amount', 'order_date']
