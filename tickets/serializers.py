from rest_framework import serializers
from tickets.models import CrawledData


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawledData
        fields = '__all__'