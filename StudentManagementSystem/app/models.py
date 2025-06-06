from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse   

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.IntegerField()
    section = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()

    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

class Grade(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    activity = models.FloatField()
    quiz = models.FloatField()
    mid_term_exam = models.FloatField()
    final_exam = models.FloatField()
    avg_grade = models.FloatField()

    def __str__(self):
        return f"{self.subject.name} - Grades"

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

#Check if the file is a valid type for uploading documents
def validate_file_type(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png','.doc', '.docx', '.txt','.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file type.')

class Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title