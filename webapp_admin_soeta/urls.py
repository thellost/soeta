from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("download", views.download_file, name="download"),
    path("reports", views.reports, name="reports"),
    path("employees.json", views.listing_api, name="employees-api"),
    path("template.json", views.listing_template, name="template-api"),
    path('select2_user.json', views.select2_user, name="select2-user")
]