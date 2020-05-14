from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
from django.shortcuts import reverse
from django.conf.urls import url
from .models import Exercise, Submission, TestResult, ExerciseResource


admin.site.register(Submission)
admin.site.register(TestResult)


class ExerciseResourceInline(admin.StackedInline):
    model = ExerciseResource


class ExerciseAdmin(admin.ModelAdmin):
    inlines = (ExerciseResourceInline,)
    readonly_fields = (
        "description_link",
        "tests_link",
        "resources_link",
        "page_link",
        "number",
    )
    fields = [field.name for field in Exercise._meta.fields] + [
        "description_link",
        "tests_link",
        "resources_link",
        "page_link",
    ]

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
            url(
                r"^download-resources/(?P<pk>\d+)$",
                self.download_resources,
                name="exercises_exercise_download-resources",
            ),
        ]
        return urls

    def description_link(self, obj):
        if obj.description:
            return format_html(
                '<a href="{}">Download</a>',
                reverse(
                    "admin:exercises_exercise_download-description",
                    args=[obj.pk],
                ),
            )
        else:
            return "Noch keine Datei hochgeladen!"

    def tests_link(self, obj):
        if obj.tests:
            return format_html(
                '<a href="{}">Download</a>',
                reverse(
                    "admin:exercises_exercise_download-tests", args=[obj.pk]
                ),
            )
        else:
            return "Noch keine Datei hochgeladen!"

    def resources_link(self, obj):
        if obj.resources:
            return format_html(
                '<a href="{}">Download</a>',
                reverse(
                    "admin:exercises_exercise_download-resources",
                    args=[obj.pk],
                ),
            )
        else:
            return "Noch keine Datei hochgeladen!"

    description_link.short_description = "Download Description"
    tests_link.short_description = "Download Tests"
    resources_link.short_description = "Download Resources"

    def download_description(self, request, pk):
        response = HttpResponse(content_type="application/force-download")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="description.md"'
        response.write(Exercise.objects.get(pk=pk).description.read())
        return response

    def download_tests(self, request, pk):
        response = HttpResponse(content_type="application/force-download")
        response["Content-Disposition"] = 'attachment; filename="tests.py"'
        response.write(Exercise.objects.get(pk=pk).tests.read())
        return response

    def download_resources(self, request, pk):
        response = HttpResponse(content_type="application/force-download")
        response["Content-Disposition"] = 'attachment; filename="resources.py"'
        response.write(Exercise.objects.get(pk=pk).resources.read())
        return response

    def page_link(self, obj):
        if obj.pk:
            return format_html(
                '<a href="{}">Link</a>', obj.get_absolute_url(),
            )
        else:
            return "Noch keine Datei hochgeladen!"

    page_link.short_description = "Zur Aufgabenseite"


admin.site.register(Exercise, ExerciseAdmin)
