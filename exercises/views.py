from django.shortcuts import render, redirect
from django.contrib import messages
from exercises.models import Exercise
from exercises.forms import SubmissionForm
from accounts.forms import LoginForm


def home_page(request):
    exercises = Exercise.objects.all()
    login = request.POST.get('login', LoginForm())
    return render(request, "home.html", {"exercises": exercises, "login": login})


def view_exercise(request, number):
    login = request.POST.get('login', LoginForm())
    try:
        exercise = Exercise.objects.get(number=number)
    except Exercise.DoesNotExist:
        return redirect(home_page)

    if not exercise.released():
        return redirect(home_page)

    form = SubmissionForm()
    if not exercise.expired and request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(request.user, exercise)
            messages.success(
                request, "Abgabe erfolgreich hochgeladen!"
            )
            return redirect(exercise)

    context = {"exercise": exercise, "form": form, "login": login}
    return render(request, "exercise.html", context)
