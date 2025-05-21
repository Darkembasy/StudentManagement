from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.IntegerField()
    section = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.first_name

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
