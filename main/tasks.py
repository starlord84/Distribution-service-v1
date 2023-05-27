from celery import shared_task
import requests
from .models import Distribution, Client


@shared_task
def send_request_to_url(distribution_id):
    distribution = Distribution.objects.get(id=distribution_id)
    clients = Client.objects.all()
    response = requests.post('https://probe.fbrq.cloud/docs/', json={'clients': clients})
