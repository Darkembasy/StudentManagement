from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class indexViewPage(TemplateView):
       template_name = 'app/index.html'

class studentViewPage(TemplateView):
       template_name = 'app/studentList.html'