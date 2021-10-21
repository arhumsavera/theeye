from django.db import models

# Create your models here.
class Event(models.Model):
    session_id = models.UUIDField()
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    # variable payload
    data = models.JSONField()
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ["-timestamp"]
        # unique_together = (session_id, timestamp,)

    def __str__(self):
        return f"{self.category}_{self.name}"


class FailedEvent(models.Model):
    session_id = models.UUIDField(null=False)
    error = models.JSONField()
    received = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.session_id)}_{self.created_at.isoformat()}"
