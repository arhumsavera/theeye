from celery import shared_task
from theeye.serializers import EventSerializer
from theeye.models import FailedEvent


@shared_task
def create_event(data):
    serializer = EventSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        error_dict = dict(serializer.errors)
        missing_fields = [
            k for k, v in error_dict.items() if v == ["This field is required."]
        ]
        for field in missing_fields:
            error_dict.pop(field)
        error_dict["missingfields"] = missing_fields

        FailedEvent.objects.create(
            session_id=data.get("session_id"),
            error=error_dict,
            received=data,
        )
