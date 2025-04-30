from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('survey/', views.survey_form, name='survey-form'),
    path('surveys/', views.survey_list, name='survey-list'),
]