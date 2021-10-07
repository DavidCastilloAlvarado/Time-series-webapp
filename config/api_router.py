
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from tswebserver.tsservices.views import ForescastApiView


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


# Time series API
router.register("model", ForescastApiView)

app_name = "api"
urlpatterns = router.urls