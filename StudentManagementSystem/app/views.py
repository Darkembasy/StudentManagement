from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.generic import TemplateView,ListView,DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from .models import Student, Subject, Grade, Post,Document
from .serializers import StudentSerializer, SubjectSerializer, GradeSerializer
from django.urls import reverse_lazy, reverse, path
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist.")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.error(request, "Username or password does not exist.")
            
    context = {}
    return render(request,'app/login_reg.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')
class SubjectListView(ListView):
    model = Subject
    template_name = 'app/subject_list.html'

    def get_queryset(self):
        self.student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        return Subject.objects.filter(student=self.student)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.student
        return context


    # Add subject for a student
class SubjectCreateView(CreateView):
    model = Subject
    fields = ['name']
    template_name = 'app/subject_form.html'

    def form_valid(self, form):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        form.instance.student = student
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('subject_list', kwargs={'student_id': self.kwargs['student_id']})

    # Update a subject
class SubjectUpdateView(UpdateView):
    model = Subject
    fields = ['name']
    template_name = 'app/subject_form.html'

    def get_success_url(self):
        return reverse('subject_list', kwargs={'student_id': self.object.student.id})

    # Delete a subject
class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'app/subject_delete.html'

    def get_success_url(self):
        return reverse('subject_list', kwargs={'student_id': self.object.student.id})

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

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/post_list.html'

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/post_detail.html'


