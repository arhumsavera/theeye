from django.utils.dateparse import parse_datetime

from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    # queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()

        session_id = self.request.query_params.get("session_id")
        name = self.request.query_params.get("name")
        category = self.request.query_params.get("category")
        start_datetime = self.request.query_params.get("start_datetime")
        end_datetime = self.request.query_params.get("end_datetime")

        if start_datetime is not None:
            start_datetime = parse_datetime(start_datetime)
        if end_datetime is not None:
            end_datetime = parse_datetime(end_datetime)

        if session_id is not None:
            queryset = queryset.filter(session_id=session_id)
        if category is not None:
            queryset = queryset.filter(category=category)
        if name is not None:
            queryset = queryset.filter(name=name)
        if start_datetime is not None:
            queryset = queryset.filter(timestamp__gte=start_datetime)
        if end_datetime is not None:
            queryset = queryset.filter(timestamp__lte=end_datetime)

        return queryset
