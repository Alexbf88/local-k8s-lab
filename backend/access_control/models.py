from django.db import models


class Resident(models.Model):
    """
    Represents a permanent resident or property owner within the condominium.
    """

    name = models.CharField(max_length=150)
    document_id = models.CharField(max_length=50, unique=True)
    # Using CharField for house numbers to safely support formats like '12A' or '14-B'
    house_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (House {self.house_number})"


class Vehicle(models.Model):
    """
    Represents a vehicle tied to a specific resident.
    A resident can own multiple vehicles.
    """

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="vehicles")
    plate = models.CharField(max_length=15, unique=True)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.model} [{self.plate}]"


class Employee(models.Model):
    """
    Represents the staff working at the gated community (e.g., security, administration).
    """

    name = models.CharField(max_length=150)
    document_id = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=100)  # e.g., 'Security Guard', 'Janitor'
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.role}"


class AccessLog(models.Model):
    """
    The core ledger recording all physical entrance events at the main gate.
    Tracks residents, employees, or external visitors.
    """

    CATEGORY_CHOICES = [
        ("RESIDENT", "Resident"),
        ("EMPLOYEE", "Employee"),
        ("VISITOR", "Visitor/Delivery"),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    # Relationships are optional (null=True) to accommodate manual visitor entries
    resident = models.ForeignKey(Resident, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

    # Visitor fields (used if category is 'VISITOR')
    visitor_name = models.CharField(max_length=150, null=True, blank=True)
    visitor_document_id = models.CharField(max_length=50, null=True, blank=True)

    # Snapshot of vehicle data at the exact moment of entry
    vehicle_plate = models.CharField(max_length=15, null=True, blank=True)
    vehicle_info = models.CharField(max_length=200, null=True, blank=True)  # Model and Color combined

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.category} Entry"
