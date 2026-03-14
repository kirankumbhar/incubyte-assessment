from rest_framework import serializers
from .models import Employee
 
 
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "full_name", "job_title", "country", "salary", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
 
 
class SalaryCalculationSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    full_name = serializers.CharField()
    country = serializers.CharField()
    gross_salary = serializers.DecimalField(max_digits=12, decimal_places=2)
    deductions = serializers.DictField(child=serializers.DecimalField(max_digits=12, decimal_places=2))
    net_salary = serializers.DecimalField(max_digits=12, decimal_places=2)

class SalaryMetricsByCountrySerializer(serializers.Serializer):
    country = serializers.CharField()
    min_salary = serializers.DecimalField(max_digits=12, decimal_places=2)
    max_salary = serializers.DecimalField(max_digits=12, decimal_places=2)
    average_salary = serializers.DecimalField(max_digits=12, decimal_places=2)
 
 
class SalaryMetricsByJobTitleSerializer(serializers.Serializer):
    job_title = serializers.CharField()
    average_salary = serializers.DecimalField(max_digits=12, decimal_places=2)