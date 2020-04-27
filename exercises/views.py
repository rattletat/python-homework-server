from django.shortcuts import render, redirect
from exercises.models import Exercise, Submission
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

    submission = Submission(exercise=exercise)

    if request.method == "GET":
        form = SubmissionForm(instance=submission)

    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES, instance=submission)

        if form.is_valid():
            form.save()
            return redirect(exercise)

    # Exercise.objects.create(number=5, description="""
    context = {"exercise": exercise, "form": form}
    return render(request, "exercise.html", context)
