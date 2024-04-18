from django.urls import path
from . import views

urlpatterns = [
    path('contrast/xlsx', views.ContrastExcelFiles, name="contrast-xlsx"),
    path('contrast/csv', views.ContrastCsvFiles, name="contrast-csv"),
    path('contrast/larges-csv', views.ContrastLargeCsvFiles, name="contrast-larges-csv"),
    
    path('contrast/large-csv', views.ContrastLargeCsvFile, name="contrast-large-csv")
]