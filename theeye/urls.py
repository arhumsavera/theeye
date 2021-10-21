from rest_framework import routers
from .views import EventViewSet

router = routers.SimpleRouter()
router.register("events", EventViewSet, basename="events")


urlpatterns = router.urls
