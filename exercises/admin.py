from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import reverse
from django.conf.urls import url
from .models import Exercise, Submission, TestResult, ExerciseResource


class TestResultInline(admin.StackedInline):
    model = TestResult
    readonly_fields = (
        "first_error",
        "first_failure",
    )


class SubmissionAdmin(admin.ModelAdmin):
    inlines = [TestResultInline]
    readonly_fields = (
        "uploaded",
        "exercise",
        "user",
        "file",
        "submission_link",
    )

    def get_urls(self):
        urls = super(SubmissionAdmin, self).get_urls()
        urls += [
            url(
                r"^download-submission/(?P<pk>\d+)$",
                self.download_submission,
                name="exercises_submission_download-submission",
            ),
        ]
        return urls

    def submission_link(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}">Download</a>',
                reverse("admin:exercises_submission_download-submission", args=[obj.pk],),
            )
        else:
            return "Noch keine Datei hochgeladen!"

    submission_link.short_description = "Download Submission"

    @method_decorator(staff_member_required)
    def download_submission(self, request, pk):
        response = HttpResponse(content_type="application/force-download")
        response["Content-Disposition"] = 'attachment; filename="submission.py"'
        response.write(Submission.objects.get(pk=pk).file.read())
        return response


admin.site.register(Submission, SubmissionAdmin)


class ExerciseResourceInline(admin.StackedInline):
    model = ExerciseResource


class ExerciseAdmin(admin.ModelAdmin):
    inlines = (ExerciseResourceInline,)
    readonly_fields = (
        "description_link",
        "tests_link",
        "resources_link",
        "number",
    )
    fields = [field.name for field in Exercise._meta.fields] + [
        "description_link",
        "tests_link",
        "resources_link",
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
                r"^download-test/(?P<pk>\d+)$",
                self.download_test,
                name="exercises_exercise_download-test",
            ),
            url(
                r"^download-resource/(?P<pk>\d+)$",
                self.download_resource,
                name="exercises_exercise_download-resource",
            ),
        ]
        return urls

    def description_link(self, obj):
        download_view = "admin:exercises_exercise_download-description"
        if obj.description:
            return format_html(
                '<a href="{}">Download</a>', reverse(download_view, args=[obj.pk],),
            )
        else:
            return "Noch keine Datei hochgeladen!"

    def tests_link(self, obj):
        download_view = "admin:exercises_exercise_download-test"
        if obj.tests:
            return format_html(
                '<a href="{}">Download</a>', reverse(download_view, args=[obj.pk]),
            )
        else:
            return "Noch keine Datei hochgeladen!"

    def resources_link(self, obj):
        resources = ExerciseResource.objects.filter(exercise=obj)
        if resources:
            download_view = "admin:exercises_exercise_download-resource"
            generator = (
                (reverse(download_view, args=[resource.pk]), resource.file.name)
                for resource in resources
            )
            buttons = format_html_join(
                " ", "<a href='{}'>Download: {}</a><br><br>", generator
            )
            return buttons
        else:
            return "Noch keine Datei(en) hochgeladen!"

    description_link.short_description = "Download Description"
    tests_link.short_description = "Download Tests"
    resources_link.short_description = "Download Resources"

    @method_decorator(staff_member_required)
    def download_description(self, request, pk):
        response = HttpResponse(content_type="application/force-download")
        response["Content-Disposition"] = 'attachment; filename="description.md"'
        response.write(Exercise.objects.get(pk=pk).description.read())
        return response

    @method_decorator(staff_member_required)
    def download_test(self, request, pk):
        response = HttpResponse(content_type="application/force-download")
        response["Content-Disposition"] = 'attachment; filename="tests.py"'
        response.write(Exercise.objects.get(pk=pk).tests.read())
        return response

    @method_decorator(staff_member_required)
    def download_resource(self, request, pk):
        response = HttpResponse(content_type="application/force-download")
        response["Content-Disposition"] = 'attachment; filename="resource.py"'
        response.write(ExerciseResource.objects.get(pk=pk).file.read())
        return response


admin.site.register(Exercise, ExerciseAdmin)
