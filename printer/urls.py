from django.urls import path
from .views import GetCheckView

urlpatterns = [
    path('api/v1/get-check-view/', GetCheckView.as_view()),
]