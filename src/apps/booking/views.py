from django.shortcuts import render
from django.views.generic import DetailView

from apps.schedule.models import Schedule


# Create your views here.
class BookingDetailView(DetailView):
    model = Schedule
    context_object_name = 'session'
