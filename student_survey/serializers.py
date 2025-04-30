from rest_framework import serializers
from .models import StudentSurvey

class StudentSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSurvey
        fields = '__all__'