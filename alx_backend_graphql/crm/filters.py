import django_filters
from .models import Customer

class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = {
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'phone': ['exact', 'icontains'],
        }
