from django.shortcuts import render, redirect
from django.db.models import FloatField, F
from django.db.models.functions import Cast
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from exercises.models import Exercise, Submission, TestResult, TestMessage
from exercises.forms import SubmissionForm
from accounts.forms import LoginForm
from exercises.tasks import compute_test_result
from exercises.queries import get_user_test_results
import django_rq

UPLOAD_SUCCESS = "Abgabe erfolgreich hochgeladen! Das Ergebnis müsste bald auftauchen!"


def home_page(request):
    exercises = Exercise.objects.all()
    login = request.POST.get("login", LoginForm())
    return render(request, "home.html", {"exercises": exercises, "login": login})


def view_exercise(request, number):
    try:
        exercise = Exercise.objects.get(number=number)
    except Exercise.DoesNotExist:
        return redirect("home")

    if not exercise.released():
        return redirect("home")

    if request.method == "POST":
        submission = Submission(exercise=exercise, user=request.user)
        form = SubmissionForm(request.POST, request.FILES, instance=submission)

        if form.is_valid():
            form.save()
            django_rq.enqueue(compute_test_result, submission)
            messages.success(request, UPLOAD_SUCCESS)
            return redirect(exercise)
        else:
            for error in form.errors.values():
                messages.error(request, error[0])

    login = request.POST.get("login", LoginForm())
    context = {
        "exercise": exercise,
        "form": SubmissionForm(),
        "login": login,
    }

    if request.user.is_authenticated:
        tests = get_user_test_results(request.user, exercise)
        if tests:
            context["result"] = (
                tests.exclude(test_count=0)
                .annotate(
                    success_rate=Cast(F("success_count") * 100, FloatField())
                    / Cast(F("test_count"), FloatField())
                )
                .values("success_rate", "test_count", "success_count")
                .order_by("-success_rate")[0]
            )

    return render(request, "exercise.html", context)


@login_required
def view_results(request, number):
    exercise = Exercise.objects.get(number=number)
    tests = get_user_test_results(request.user, exercise, add_messages=True)

    context = {"exercise": exercise, "results": tests}
    return render(request, "result.html", context)
