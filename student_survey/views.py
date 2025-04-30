from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import StudentSurvey
from .serializers import StudentSurveySerializer

class StudentSurveyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for student surveys
    """
    queryset = StudentSurvey.objects.all().order_by('-date_of_survey')
    serializer_class = StudentSurveySerializer

@api_view(['GET'])
def get_survey_list(request):
    """
    API endpoint to get the list of surveys
    """
    surveys = StudentSurvey.objects.all().order_by('-date_of_survey')
    serializer = StudentSurveySerializer(surveys, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def submit_survey(request):
    """
    API endpoint to submit a new survey
    """
    serializer = StudentSurveySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_survey_detail(request, pk):
    """
    API endpoint to get a specific survey
    """
    try:
        survey = StudentSurvey.objects.get(pk=pk)
    except StudentSurvey.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = StudentSurveySerializer(survey)
    return Response(serializer.data)