from django.http import HttpResponseRedirect
from django.shortcuts import render
from exercises.models import Exercise

# from exercises.forms import UploadFileForm


def home_page(request):
    exercises = Exercise.objects.all()
    return render(request, "home.html", {"exercises": exercises})


def view_exercise(request, exercise_number):
    exercise = Exercise.objects.get(number=exercise_number)
    if exercise.is_started():
        return render(request, "exercise.html", {"exercise": exercise})
    else:
        return home_page(request)


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             result = handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('')
#     else:
#         form = UploadFileForm()
#     return render(request, 'exercise.html', {'form': form})
