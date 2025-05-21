from django.urls import path
from .views import indexViewPage, studentViewPage
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, SubjectViewSet, GradeViewSet


router = DefaultRouter()
router.register(r'api/students', StudentViewSet)
router.register(r'api/subjects', SubjectViewSet)
router.register(r'api/grades', GradeViewSet)

urlpatterns = [
    path('',indexViewPage.as_view(),name='index'),
    path('student/',studentViewPage.as_view(),name='student'),
    path('', include(router.urls)),
]
