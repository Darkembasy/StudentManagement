from django.urls import path
from .views import indexViewPage, studentViewPage

urlpatterns = [
    path('',indexViewPage.as_view(),name='index'),
    path('student/',studentViewPage.as_view(),name='student'),
]
