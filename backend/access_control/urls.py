from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResidentViewSet, VehicleViewSet, EmployeeViewSet, AccessLogViewSet

# Initialize the DefaultRouter for automated RESTful URL generation
router = DefaultRouter()
router.register(r"residents", ResidentViewSet, basename="resident")
router.register(r"vehicles", VehicleViewSet, basename="vehicle")
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"access-logs", AccessLogViewSet, basename="access-log")

# The API URLs are now determined automatically by the router
urlpatterns = [
    path("", include(router.urls)),
]
