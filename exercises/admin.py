from django.contrib import admin

from .models import Exercise, Submission, TestResult, TestMessage

admin.site.register(Exercise)
admin.site.register(Submission)


class TestResultInline(admin.StackedInline):
    model = TestMessage
    show_change_link = True


class TestResultAdmin(admin.ModelAdmin):
    inlines = [
        TestResultInline,
    ]


admin.site.register(TestMessage)
admin.site.register(TestResult, TestResultAdmin)
