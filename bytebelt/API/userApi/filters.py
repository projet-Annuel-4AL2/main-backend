import django_filters
from .models import CustomUser

class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = ['email']
