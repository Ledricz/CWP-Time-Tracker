from rest_framework.routers import DefaultRouter
from .views import ProjectsViewSet, EntriesViewSet


router = DefaultRouter()
router.register(r"projects", ProjectsViewSet, basename="users")
router.register(r"entries", EntriesViewSet, basename="users")
urlpatterns = router.urls