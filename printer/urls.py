from django.urls import path
from .views import GetCheckView, AddPrinterView, EditPrinterView, DeletePrinterView

urlpatterns = [
    path('api/v1/get-check-view/', GetCheckView.as_view()),
    path('api/v1/add-printer-view/', AddPrinterView.as_view()),
    path('api/v1/edit-printer-view/', EditPrinterView.as_view()),
    path('api/v1/delete-printer-view/', DeletePrinterView.as_view()),   
]