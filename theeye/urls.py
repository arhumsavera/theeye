from rest_framework import routers
from .views import EventViewSet, FailedEventViewSet

router = routers.SimpleRouter()
router.register("events", EventViewSet, basename="events")
router.register("errors", FailedEventViewSet, basename="errors")


urlpatterns = router.urls
