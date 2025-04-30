from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentSurveyViewSet, get_survey_list, submit_survey, get_survey_detail

router = DefaultRouter()
router.register(r'surveys', StudentSurveyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('surveys/', get_survey_list, name='survey-list'),
    path('surveys/submit/', submit_survey, name='submit-survey'),
    path('surveys/<int:pk>/', get_survey_detail, name='survey-detail'),
]