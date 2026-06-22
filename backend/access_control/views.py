from rest_framework import viewsets, filters
from .models import Resident, Vehicle, Employee, AccessLog
from .serializers import (
    ResidentSerializer,
    VehicleSerializer,
    EmployeeSerializer,
    AccessLogSerializer,
)


class ResidentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Residents to be viewed or edited.
    Includes search capabilities by name and house number.
    """

    queryset = Resident.objects.all().order_by("-created_at")
    serializer_class = ResidentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "house_number", "document_id"]


class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Resident Vehicles to be managed.
    """

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["plate", "model"]


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Condominium Staff records to be managed.
    """

    queryset = Employee.objects.all().order_by("name")
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "document_id", "role"]


class AccessLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and creating entrance logs at the gate.
    Logs are strictly ordered by the most recent timestamp.
    """

    queryset = AccessLog.objects.all().order_by("-timestamp")
    serializer_class = AccessLogSerializer
    filter_backends = [filters.SearchFilter]
    # Allows guards or admins to quickly search logs by visitor info or vehicle plate
    search_fields = ["category", "visitor_name", "vehicle_plate"]
