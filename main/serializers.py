from rest_framework import serializers
from .models import Message, Distribution, Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = '__all__'


class DetailedMessageStatsSerializer(serializers.ModelSerializer):
    client_number = serializers.CharField(source='client.phone_number')

    class Meta:
        model = Message
        fields = ('creation_date', 'status', 'client_number')
