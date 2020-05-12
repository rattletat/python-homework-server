from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
from django.shortcuts import reverse
from django.conf.urls import url
from .models import Exercise, Submission, TestResult


admin.site.register(Submission)
admin.site.register(TestResult)


class ExerciseAdmin(admin.ModelAdmin):
    readonly_fields = ("description_link", "tests_link")
    fields = [field.name for field in Exercise._meta.fields] + ["description_link", "tests_link"]

    def get_urls(self):
        urls = super(ExerciseAdmin, self).get_urls()
        urls += [
            url(
                r"^download-description/(?P<pk>\d+)$",
                self.download_description,
                name="exercises_exercise_download-description",
            ),
            url(
                r"^download-tests/(?P<pk>\d+)$",
                self.download_tests,
                name="exercises_exercise_download-tests",
            ),
        ]
        return urls

    def description_link(self, obj):
        if obj.pk:
            return format_html(
                '<a href="{}">Download</a>',
                reverse("admin:exercises_exercise_download-description", args=[obj.pk]),
            )
        else:
            return "Noch keine Datei hochgeladen!"

    description_link.short_description = "Download Description"

    def tests_link(self, obj):
        if obj.pk:
            return format_html(
                '<a href="{}">Download</a>',
                reverse("admin:exercises_exercise_download-tests", args=[obj.pk]),
            )
        else:
            return "Noch keine Datei hochgeladen!"

    tests_link.short_description = "Download Tests"

    def download_description(self, request, pk):
        response = HttpResponse(content_type="application/force-download")
        response["Content-Disposition"] = 'attachment; filename="description.md"'
        response.write(Exercise.objects.get(pk=pk).description.read())
        return response

    def download_tests(self, request, pk):
        response = HttpResponse(content_type="application/force-download")
        response["Content-Disposition"] = 'attachment; filename="tests.py"'
        response.write(Exercise.objects.get(pk=pk).tests.read())
        return response


admin.site.register(Exercise, ExerciseAdmin)
