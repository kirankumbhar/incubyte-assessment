from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Employee
from .serializers import (
    EmployeeSerializer,
    SalaryCalculationSerializer,
)
from .services import calculate_salary

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
 
    @action(detail=True, methods=["get"], url_path="salary")
    def salary(self, request, pk=None):
        employee = self.get_object()  # raises 404 automatically
        result = calculate_salary(employee.salary, employee.country)
        data = {
            "employee_id": employee.id,
            "full_name": employee.full_name,
            "country": employee.country,
            **result,
        }
        serializer = SalaryCalculationSerializer(data)
        return Response(serializer.data)