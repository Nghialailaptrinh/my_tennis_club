from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("members/", views.members, name="members"),
    path("members/details/<slug:slug>", views.details, name="details"),
    path("testing/", views.testing, name="testing"),
    path("classes/", views.classes, name="classes"),
    path("classes/<int:pk>/", views.class_details, name="class_details"),
    path("teachers/", views.teachers, name="teachers"),
    path("teachers/<int:pk>/", views.teacher_details, name="teacher_details"),
    path("library/", views.library, name="library"),
]
