from django.urls import path
from . import views

urlpatterns = [
        path('', views.employ),
        path('?chunk=()', views.employ)
        ]
