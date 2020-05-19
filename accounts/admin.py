from django.contrib import admin

from accounts.models import User
from exercises.models import Submission


class SubmissionInline(admin.StackedInline):
    model = Submission
    show_change_link = True
    readonly_fields = ("file", "exercise", "uploaded")
    ordering = ("-uploaded",)


class UserAdmin(admin.ModelAdmin):
    fields = ("last_login", "email", "identifier")
    readonly_fields = ["last_login"]
    inlines = [
        SubmissionInline,
    ]


admin.site.register(User, UserAdmin)
