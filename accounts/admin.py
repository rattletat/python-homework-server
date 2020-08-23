from django.contrib import admin

from accounts.models import User
from exercises.models import Submission, Exercise
from exercises.queries import get_user_test_statistics, convert_points_to_grade


class SubmissionInline(admin.StackedInline):
    model = Submission
    show_change_link = True
    readonly_fields = ("file", "exercise", "uploaded")
    ordering = ("-uploaded",)


class UserAdmin(admin.ModelAdmin):
    fields = ("last_login", "email", "identifier", "points", "grade")
    list_display = ("email", "identifier", "points", "grade")
    readonly_fields = ["last_login"]
    inlines = [
        SubmissionInline,
    ]

    def points(self, obj):
        return sum(
            get_user_test_statistics(obj, exercise)['success_count']
            for exercise in Exercise.objects.all()
        )

    def grade(self, obj):
        return convert_points_to_grade(self.points(obj))


admin.site.register(User, UserAdmin)
