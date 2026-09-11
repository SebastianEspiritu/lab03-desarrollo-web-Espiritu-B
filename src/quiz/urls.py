from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('exam/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('exam/<int:exam_id>/add-question/', views.question_create, name='question_create'),
]