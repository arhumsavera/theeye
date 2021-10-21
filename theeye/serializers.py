from django.utils import timezone
from rest_framework import serializers

from .models import Event
from .validations import payload_validation_dict

# TODO prevent DELETE
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    # TODO validation
    def validate(self, data):
        try:
            dict(data["data"])
            c = data["category"]
            n = data["name"]
            key = f"{c}_{n}"
            if key in payload_validation_dict and not payload_validation_dict[key](
                data["data"]
            ):
                raise
        except Exception:
            raise serializers.ValidationError("Invalid payload for this event type")

        return data

    def validate_timestamp(self, timestamp):
        if timestamp > timezone.now():
            raise serializers.ValidationError(
                "Timestamp cannot be ahead of current time"
            )
        return timestamp
