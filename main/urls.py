from django.urls import path, include
from .views import *
from rest_framework import routers
from .views import ClientViewSet

router = routers.SimpleRouter()
router.register(r"client", ClientViewSet, basename="client")
router.register(r"distribution", DistributionViewSet, basename="distribution")

urlpatterns = [
    path("api/", include(router.urls)),
    path('api/statistics/', DistributionCommonStats.as_view(), name='overall-statistics'),
    path('api/statistics/<int:distribution_id>/', DetailedMessageStats.as_view(), name='detailed-statistics'),
    path('api/active_messages/', ActiveMessages.as_view(), name='active_messages'),
    ]
