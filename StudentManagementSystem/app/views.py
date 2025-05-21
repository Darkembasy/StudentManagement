from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from .models import Student, Subject, Grade
from .serializers import StudentSerializer, SubjectSerializer, GradeSerializer
from django.urls import reverse_lazy

# Create your views here.

class SubjectListView(ListView):
    model = Subject
    template_name = 'app/subject_list.html'

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Subject.objects.filter(student__id=student_id)

class GradeDetailView(DetailView):
    model = Grade
    template_name = 'app/grade_detail.html'


class GradeCreateView(CreateView):
    model = Grade
    fields = ['subject', 'activity', 'quiz', 'mid_term_exam','final_exam','avg_grade']
    template_name = 'app/grade_form.html'
    success_url = reverse_lazy('student_list')  # or redirect to grade list if you have one

class GradeUpdateView(UpdateView):
    model = Grade
    fields = ['activity', 'quiz', 'mid_term_exam','final_exam','avg_grade']
    template_name = 'app/grade_form.html'
    success_url = reverse_lazy('student_list')
class indexViewPage(TemplateView):
       template_name = 'app/base.html'

class studentViewPage(TemplateView):
       template_name = 'app/student_list.html'

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class StudentListView(ListView):
    model = Student
    template_name = 'app/student_list.html'

class StudentDetailView(DetailView):
    model = Student
    template_name = 'app/student_detail.html'

class StudentCreateView(CreateView):
    model = Student
    fields = ['first_name','last_name','student_id','section', 'age', 'email']
    template_name = 'app/student_form.html'
    success_url = reverse_lazy('student_list')

class StudentUpdateView(UpdateView):
    model = Student
    fields = ['first_name','last_name','student_id','student_id', 'age', 'email']
    template_name = 'app/student_form.html'
    success_url = reverse_lazy('student_list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'app/student_delete.html'
    success_url = reverse_lazy('student_list')

