from django.shortcuts import render, redirect
from exercises.models import Exercise
from exercises.forms import SubmissionForm


def home_page(request):
    exercises = Exercise.objects.all()
    return render(request, "home.html", {"exercises": exercises})


def view_exercise(request, number):
    try:
        exercise = Exercise.objects.get(number=number)
    except Exercise.DoesNotExist:
        return redirect(home_page)

    if not exercise.released():
        return redirect(home_page)

    form = SubmissionForm()
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(request.user, exercise)
            return redirect(exercise)

    context = {"exercise": exercise, "form": form}
    return render(request, "exercise.html", context)
