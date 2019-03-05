from labbyims.models import Product_Unit, Location, Room, Reserve, User
import django_filters


class ProductFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Product_Unit
        fields = ['description',]

class LocationFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Location
        fields = ['name',]

class Prod_ResFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model =  Reserve
        fields = ['description',]
