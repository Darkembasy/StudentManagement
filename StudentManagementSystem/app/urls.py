from django.urls import path
from .views import indexViewPage

urlpatterns = [
    path('',indexViewPage.as_view(),name='index'),
]
