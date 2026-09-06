from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import ClassRoom, Member, Teacher


def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template("all_members.html")
    context = {
        "mymembers": mymembers,
    }
    return HttpResponse(template.render(context, request))


def details(request, slug):
    mymember = Member.objects.get(slug=slug)
    template = loader.get_template("details.html")
    context = {
        "mymember": mymember,
    }
    return HttpResponse(template.render(context, request))


def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())


def testing(request):
    mydata = Member.objects.all()
    template = loader.get_template("template.html")
    context = {
        "mymembers": mydata,
    }
    return HttpResponse(template.render(context, request))


def classes(request):
    return render(request, "all_classes.html", {
        "classes": ClassRoom.objects.select_related("teacher").order_by("name", "pk"),
    })


def class_details(request, pk):
    classroom = get_object_or_404(
        ClassRoom.objects.select_related("teacher").prefetch_related("members"), pk=pk
    )
    return render(request, "class_details.html", {"classroom": classroom})


def teachers(request):
    return render(request, "all_teachers.html", {
        "teachers": Teacher.objects.order_by("firstname", "lastname", "pk"),
    })


def teacher_details(request, pk):
    teacher = get_object_or_404(Teacher.objects.prefetch_related("classes"), pk=pk)
    return render(request, "teacher_details.html", {"teacher": teacher})


def library(request):
    return render(request, "library.html")
