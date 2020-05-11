from django.contrib import admin

from .models import Exercise, Submission, TestResult, TestMessage

admin.site.register(Exercise)
admin.site.register(Submission)
admin.site.register(TestResult)
admin.site.register(TestMessage)
