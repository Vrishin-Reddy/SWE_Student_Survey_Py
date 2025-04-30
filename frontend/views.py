from django.shortcuts import render
from django.conf import settings  # <-- add this line

def index(request):
    """
    View for the home page
    """
    return render(request, 'frontend/index.html')

def survey_form(request):
    """
    View for the survey form page
    """
    return render(request, 'frontend/survey_form.html')

def survey_list(request):
    """
    View for the survey list page
    """
    return render(request, 'frontend/survey_list.html', {
        'API_BASE_URL': settings.API_BASE_URL  # <-- inject API base URL here
    })
