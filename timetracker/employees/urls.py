from rest_framework.routers import DefaultRouter
from .views import EmployeesViewSet


router = DefaultRouter()
router.register(r"employees", EmployeesViewSet, basename="employees")
urlpatterns = router.urls