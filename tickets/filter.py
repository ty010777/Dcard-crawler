from django import forms
from .models import CrawledData
import django_filters


class DataFilter(django_filters.FilterSet):

    cTitle = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput())

    cForumName = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput())

    cTag = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput())
    cContent = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput())
    class Meta:
        model = CrawledData
        fields = ['cTitle', 'cForumName','cTag','cContent']
