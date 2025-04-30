from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('student_survey.urls')),
    path('', include('frontend.urls')),
]