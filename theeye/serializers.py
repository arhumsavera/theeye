from rest_framework import serializers

from .models import Event

# TODO prevent DELETE
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    # TODO validation
