from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Employee
from .serializers import (
    EmployeeSerializer,
    SalaryCalculationSerializer,
    SalaryMetricsByCountrySerializer,
    SalaryMetricsByJobTitleSerializer
)
from .services import calculate_salary, get_metrics_by_country, get_avg_salary_by_job_title

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

class SalaryMetricsByCountryView(APIView):
    def get(self, request):
        country = request.query_params.get("country", "").strip()
        if not country:
            return Response(
                {"detail": "Query parameter 'country' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = get_metrics_by_country(country)
        if result is None:
            return Response(
                {"detail": f"No employees found for country '{country}'."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SalaryMetricsByCountrySerializer(result)
        return Response(serializer.data)


class SalaryMetricsByJobTitleView(APIView):
    def get(self, request):
        job_title = request.query_params.get("job_title", "").strip()
        if not job_title:
            return Response(
                {"detail": "Query parameter 'job_title' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = get_avg_salary_by_job_title(job_title)
        if result is None:
            return Response(
                {"detail": f"No employees found for job title '{job_title}'."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SalaryMetricsByJobTitleSerializer(result)
        return Response(serializer.data)