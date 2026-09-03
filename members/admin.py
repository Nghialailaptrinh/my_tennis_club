from django.contrib import admin
from .models import Member

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
