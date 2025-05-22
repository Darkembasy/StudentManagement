from django.contrib import admin
from .models import Student, Subject, Grade, Post, Document

# Register your models here.
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Post)
admin.site.register(Document)