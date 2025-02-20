from django.urls import path
from .views import Give_Check

urlpatterns = [
    path('api/v1/get-check/', Give_Check.as_view()),
]
