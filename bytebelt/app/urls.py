from django.urls import path
from . import views

urlpatterns = [
    path('execute-code/', views.execute_code, name='execute_code'),
]
