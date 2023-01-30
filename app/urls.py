from django.urls import path
from .views import *


urlpatterns = [
    path('v1/calendar/init/', GoogleCalendarInitView.as_view()),
    path('v1/calendar/redirect/', GoogleCalendarRedirectView.as_view())
]