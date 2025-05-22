from django.urls import path
from .views import indexViewPage, studentViewPage
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, SubjectViewSet, GradeViewSet, PostListView
from .views import *


router = DefaultRouter()
router.register(r'api/students', StudentViewSet)
router.register(r'api/subjects', SubjectViewSet)
router.register(r'api/grades', GradeViewSet)

urlpatterns = [
    path('',indexViewPage.as_view(),name='base'),

    path('', include(router.urls)),
    path('studentlist/', StudentListView.as_view(), name='student_list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('students/create/', StudentCreateView.as_view(), name='student_create'),
    path('students/<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
    path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),

    path('students/<int:student_id>/subjects/', SubjectListView.as_view(), name='subject_list'),

    path('grades/<int:pk>/', GradeDetailView.as_view(), name='grade_detail'),
    path('grades/create/', GradeCreateView.as_view(), name='grade_create'),
    path('grades/<int:pk>/update/', GradeUpdateView.as_view(), name='grade_update'),

    #Post
    path('post/', PostListView.as_view(), name='post'),
]
