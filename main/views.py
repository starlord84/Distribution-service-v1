from django.db.models import Count
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import ClientSerializer, DistributionSerializer, DetailedMessageStatsSerializer
from .models import Client, Message, Distribution
from rest_framework.response import Response
import requests
from rest_framework import status


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        client = serializer.save()
        current_time = timezone.now()

        distributions = Distribution.objects.filter(
            start_date__lte=current_time,
            due_date__gte=current_time,
            tag=client.tag
        )

        clients = Client.objects.filter(
            distribution__in=distributions
        )

        client_serializer = ClientSerializer(clients, many=True)
        client_data = client_serializer.data

        try:
            response = requests.post("https://probe.fbrq.cloud/docs/", json=client_data)
            response.raise_for_status()
            return Response({'status': 'Запрос отправлен успешно'})
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DistributionViewSet(viewsets.ModelViewSet):
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer


class DistributionCommonStats(APIView):
    def get(self, request):
        distribution_count = Distribution.objects.count()
        message_stats = Message.objects.values('status').annotate(count=Count('status'))
        statistics_data = {
            'distribution_count': distribution_count,
            'message_stats': message_stats
        }
        return Response(statistics_data)


class DetailedMessageStats(APIView):
    def get(self, request, distribution_id):
        messages = Message.objects.filter(distribution_id=distribution_id)
        serializer = DetailedMessageStatsSerializer(messages, many=True)
        distribution = Distribution.objects.get(id=distribution_id)
        data = serializer.data
        data_with_distribution = {
            'distribution': distribution.text,
            'messages': data
        }
        return Response(data_with_distribution)


class ActiveMessages(APIView):
    def get(self, request):
        clients = Client.objects.filter(message__status=True)
        serialized_clients = ClientSerializer(clients, many=True)
        return Response(serialized_clients.data)

