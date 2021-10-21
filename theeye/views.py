from django.utils.dateparse import parse_datetime
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Event, FailedEvent
from .serializers import EventSerializer, FailedEventSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def create(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            error_dict = dict(serializer.errors)
            missing_fields = [
                k for k, v in error_dict.items() if v == ["This field is required."]
            ]
            for field in missing_fields:
                error_dict.pop(field)
            error_dict["missingefields"] = missing_fields

            FailedEvent.objects.create(
                session_id=request.data.get("session_id"),
                error=error_dict,
                received=request.data,
            )
        return Response(status=status.HTTP_202_ACCEPTED)

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


class FailedEventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FailedEventSerializer

    def get_queryset(self):
        queryset = FailedEvent.objects.all()
        session_id = self.request.query_params.get("session_id")
        if session_id is not None:
            queryset = queryset.filter(session_id=session_id)

        return queryset
