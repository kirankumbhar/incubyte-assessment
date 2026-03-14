from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, SalaryMetricsByCountryView, SalaryMetricsByJobTitleView


router = DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employee")

urlpatterns = [
    path("", include(router.urls)),
    path("salary-metrics/by-country/", SalaryMetricsByCountryView.as_view(), name="salary-metrics-by-country"),
    path("salary-metrics/by-job-title/", SalaryMetricsByJobTitleView.as_view(), name="salary-metrics-by-job-title"),
]
