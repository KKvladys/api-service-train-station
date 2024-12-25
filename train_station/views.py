from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from train_station.filters import (
    StationFilter,
    RouteFilter,
    TripFilter
)
from train_station.models import (
    Station,
    Route,
    TrainType,
    Train,
    Order,
    Trip,
    Ticket,
    Crew
)
from train_station.serializers import (
    CrewSerializer,
    StationSerializer,
    RouteSerializer,
    TrainSerializer,
    OrderSerializer,
    TicketSerializer,
    TripSerializer,
    TrainTypeSerializer,
    RouteListSerializer,
    TrainListSerializer,
    OrderListSerializer,
    TripListSerializer
)


class TripOrderViewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class StationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StationFilter
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RouteFilter
    queryset = Route.objects.all()

    def get_serializer_class(self):
        serializer_class = RouteSerializer
        if self.action == "list":
            return RouteListSerializer
        return serializer_class


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()

    def get_serializer_class(self):
        serializer_class = TrainSerializer
        if self.action == "list":
            return TrainListSerializer
        return serializer_class


class OrderViewSet(viewsets.ModelViewSet):
    pagination_class = TripOrderViewPagination
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        serializer_class = OrderSerializer
        if self.action == "list":
            return OrderListSerializer
        return serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TripViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TripFilter
    pagination_class = TripOrderViewPagination
    queryset = Trip.objects.all()

    def get_serializer_class(self):
        serializer_class = TripSerializer
        if self.action == "list":
            return TripListSerializer
        return serializer_class


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TrainTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
