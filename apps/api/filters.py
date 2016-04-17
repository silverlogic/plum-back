from rest_framework import filters


class FilterSet(filters.FilterSet):
    order_by_field = 'order_by'
