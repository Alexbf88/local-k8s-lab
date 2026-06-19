from rest_framework import serializers
from .models import Resident, Vehicle, Employee, AccessLog


class VehicleSerializer(serializers.ModelSerializer):
    """
    Handles serialization and validation for Resident-owned vehicles.
    """

    class Meta:
        model = Vehicle
        fields = ["id", "resident", "plate", "model", "color"]


class ResidentSerializer(serializers.ModelSerializer):
    """
    Serializes Resident data along with their associated vehicles nesting.
    """

    # Includes read-only vehicle relation to list cars directly inside the resident object
    vehicles = VehicleSerializer(many=True, read_read_only=True)

    class Meta:
        model = Resident
        fields = ["id", "name", "document_id", "house_number", "vehicles", "created_at"]


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Handles data transformation for Condominium staff members.
    """

    class Meta:
        model = Employee
        fields = ["id", "name", "document_id", "role", "is_active"]


class AccessLogSerializer(serializers.ModelSerializer):
    """
    Handles logging and auditing of physical entries at the gate.
    Includes custom validation to ensure specific data matches the selected category.
    """

    class Meta:
        model = AccessLog
        fields = [
            "id",
            "timestamp",
            "category",
            "resident",
            "employee",
            "visitor_name",
            "visitor_document_id",
            "vehicle_plate",
            "vehicle_info",
        ]

    def validate(self, data):
        """
        Custom cross-field validation to ensure structural integrity of the entry logs.
        """
        category = data.get("category")

        if category == "RESIDENT" and not data.get("resident"):
            raise serializers.ValidationError({"resident": "A valid resident reference is required for RESIDENT entries."})

        if category == "EMPLOYEE" and not data.get("employee"):
            raise serializers.ValidationError({"employee": "A valid employee reference is required for EMPLOYEE entries."})

        if category == "VISITOR":
            if not data.get("visitor_name") or not data.get("visitor_document_id"):
                raise serializers.ValidationError(
                    {"visitor_name": "Visitor name and document identity are mandatory for guest logs."}
                )

        return data
