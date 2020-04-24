from django.shortcuts import render
from exercises.models import Exercise


def home_page(request):
    exercises = Exercise.objects.all()
    return render(request, "home.html", {"exercises": exercises})


def view_exercise(request, exercise_number):
    exercise = Exercise.objects.get(number=exercise_number)
    test.error()
    return render(request, "exercise.html", {"exercise": exercise})
