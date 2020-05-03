from django.shortcuts import render, redirect
from django.contrib import messages
from exercises.models import Exercise, Submission
from exercises.forms import SubmissionForm
from accounts.forms import LoginForm

UPLOAD_SUCCESS = "Abgabe erfolgreich hochgeladen!"


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

    form = SubmissionForm()  # Move later
    if request.method == "POST":
        submission = Submission(exercise=exercise, user=request.user)
        form = SubmissionForm(request.POST, request.FILES, instance=submission)

        if form.is_valid():
            form.save()
            messages.success(request, UPLOAD_SUCCESS)
            return redirect(exercise)
        else:
            for error in form.errors.values():
                messages.error(request, error[0])

    context = {"exercise": exercise, "form": form}
    return render(request, "exercise.html", context)
