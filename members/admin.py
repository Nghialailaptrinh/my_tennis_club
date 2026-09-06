from django.contrib import admin
from .models import ClassRoom, Member, Teacher

admin.site.site_header = "My Study Club Administration"
admin.site.site_title = "My Study Club Admin"
admin.site.index_title = "Manage My Study Club"

# Register your models here.


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "firstname",
        "lastname",
        "joined_date",
    )
    prepopulated_fields = {"slug": ("firstname", "lastname")}


admin.site.register(Member, MemberAdmin)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "phone")
    search_fields = ("firstname", "lastname")


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher")
    list_filter = ("teacher",)
    search_fields = ("name", "teacher__firstname", "teacher__lastname")
    autocomplete_fields = ("teacher",)
    filter_horizontal = ("members",)
