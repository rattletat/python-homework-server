from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from exercises.models import Exercise, Submission, ExerciseResource
from exercises.forms import SubmissionForm
from accounts.forms import LoginForm
from exercises.tasks import compute_test_result
from exercises.queries import get_user_test_results, get_user_test_statistics
from django.utils.html import format_html
from sendfile import sendfile

import django_rq

UPLOAD_SUCCESS = "Abgabe erfolgreich hochgeladen! Das Ergebnis müsste bald in <a href='{}'>deinen Ergebnissen</a> auftauchen!"


def home_page(request):
    exercises = Exercise.objects.all()
    login = request.POST.get("login", LoginForm())
    context = {"exercises": exercises, "login": login}
    if request.user.is_authenticated:
        for exercise in exercises:
            exercise.statistics = get_user_test_statistics(
                request.user, exercise
            )
        context["max_points"] = sum(
            exercise.statistics["test_count"]
            for exercise in exercises
            if exercise.relevant
        )
        context["user_points"] = sum(
            exercise.statistics["success_count"]
            for exercise in exercises
            if exercise.relevant
        )
    return render(request, "home.html", context)


def view_exercise(request, number):
    try:
        exercise = Exercise.objects.get(number=number)
    except Exercise.DoesNotExist:
        return redirect("home")

    if not exercise.released() and not request.user.is_staff:
        return redirect("home")

    if request.method == "POST":
        submission = Submission(exercise=exercise, user=request.user)
        form = SubmissionForm(request.POST, request.FILES, instance=submission)

        if form.is_valid():
            form.save()
            django_rq.enqueue(compute_test_result, submission)
            messages.success(
                request, format_html(UPLOAD_SUCCESS, exercise.get_result_url())
            )
            return redirect(exercise)
        else:
            for error in form.errors.values():
                messages.error(request, error[0])

    login = request.POST.get("login", LoginForm())
    context = {
        "exercise": exercise,
        "form": SubmissionForm(),
        "login": login,
        "resources": ExerciseResource.objects.filter(exercise=exercise),
    }
    if request.user.is_authenticated:
        context["statistics"] = get_user_test_statistics(
            request.user, exercise
        )

    return render(request, "exercise.html", context)


@login_required
def view_results(request, number):
    exercise = Exercise.objects.get(number=number)
    tests = get_user_test_results(request.user, exercise)

    context = {"exercise": exercise, "tests": tests}
    return render(request, "result.html", context)


@login_required
def download_public_file(request, resource_id):
    resource = ExerciseResource.objects.get(pk=resource_id)
    if resource.exercise.released():
        return sendfile(request, resource.file.path, attachment=True)
    else:
        return redirect("home")
