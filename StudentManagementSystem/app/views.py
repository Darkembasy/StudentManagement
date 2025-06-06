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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

# Create your views here.
def loginPage(request):
    page = 'login'
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
            return redirect('student_list')
        else:
            messages.error(request, "Username or password does not exist.")
            
    context = {'page': page}
    return render(request,'app/login_reg.html', context)

@login_required
def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('base')
        else:
            messages.error(request, 'An error occurred during registration')    
    return render(request, 'app/login_reg.html', {'form': form})

class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'app/subject_list.html'
    login_url = '/login/'  # Redirect to login page if not authenticated

    def get_queryset(self):
        self.student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        return Subject.objects.filter(student=self.student)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.student
        return context

# Add subject for a student
class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    fields = ['name']
    template_name = 'app/subject_form.html'
    login_url = '/login/'

    def form_valid(self, form):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        form.instance.student = student
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('subject_list', kwargs={'student_id': self.kwargs['student_id']})

# Update a subject
class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    fields = ['name']
    template_name = 'app/subject_form.html'
    login_url = '/login/'

    def get_success_url(self):
        return reverse('subject_list', kwargs={'student_id': self.object.student.id})

# Delete a subject
class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    template_name = 'app/subject_delete.html'
    login_url = '/login/'

    def get_success_url(self):
        return reverse('subject_list', kwargs={'student_id': self.object.student.id})

class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'app/grade_list.html'
    context_object_name = 'grades'
    paginate_by = 20
    login_url = '/login/'

    def get_queryset(self):
        # Always start with all grades, optimized with select_related
        queryset = Grade.objects.all().select_related('subject', 'subject__student')
        
        # Get search query from GET parameters
        search_query = self.request.GET.get('search', '').strip()
        
        # Only filter if there's actually a search query
        if search_query:
            queryset = queryset.filter(
                Q(subject__student__first_name__icontains=search_query) |
                Q(subject__student__last_name__icontains=search_query) |
                Q(subject__student__student_id__icontains=search_query) |
                Q(subject__name__icontains=search_query)
            ).distinct()
        
        return queryset.order_by('subject__student__last_name', 'subject__student__first_name', 'subject__name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['total_grades'] = Grade.objects.count()
        return context

class GradeDetailView(LoginRequiredMixin, DetailView):
    model = Grade
    template_name = 'app/grade_detail.html'
    login_url = '/login/'

class GradeCreateView(LoginRequiredMixin, CreateView):
    model = Grade
    fields = ['student','subject', 'activity', 'quiz', 'mid_term_exam','final_exam','avg_grade']
    template_name = 'app/grade_form.html'
    success_url = reverse_lazy('student_list')
    login_url = '/login/'

class GradeUpdateView(LoginRequiredMixin, UpdateView):
    model = Grade
    fields = ['activity', 'quiz', 'mid_term_exam','final_exam','avg_grade']
    template_name = 'app/grade_form.html'
    success_url = reverse_lazy('student_list')
    login_url = '/login/'

class indexViewPage(TemplateView):
    template_name = 'app/base.html'
    # No login required for home page

class studentViewPage(LoginRequiredMixin, TemplateView):
    template_name = 'app/student_list.html'
    login_url = '/login/'

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # Note: For API views, you might want to use DRF's permission classes instead

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'app/student_list.html'
    login_url = '/login/'

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'app/student_detail.html'
    login_url = '/login/'

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    fields = ['first_name','last_name','student_id','section', 'age', 'email']
    template_name = 'app/student_form.html'
    success_url = reverse_lazy('student_list')
    login_url = '/login/'

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ['first_name','last_name','student_id','student_id', 'age', 'email']
    template_name = 'app/student_form.html'
    success_url = reverse_lazy('student_list')
    login_url = '/login/'

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'app/student_delete.html'
    success_url = reverse_lazy('student_list')
    login_url = '/login/'

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/post_list.html'
    login_url = '/login/'

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/post_detail.html'
    login_url = '/login/'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body']  # Don't include 'author' in fields
    template_name = 'app/post_create.html'
    login_url = '/login/'
   
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'body']
    template_name = 'app/post_edit.html'
    login_url = '/login/'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post   
    template_name = 'app/post_delete.html'
    success_url = reverse_lazy('post')
    login_url = '/login/'