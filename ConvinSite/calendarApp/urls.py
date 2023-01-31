from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('GoogleCalenderEvents', views.GoogleCalendarInitView, name='GoogleCalendarInitView'),
    path('GoogleCalenderEventsView', views.GoogleCalendarRedirectView, name='GoogleCalendarRedirectView')
]