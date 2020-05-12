from exercises.models import TestResult
from django.db.models import FloatField, F
from django.db.models.functions import Cast


def get_user_test_results(user, exercise):
    return TestResult.objects.filter(
        submission__user=user, submission__exercise=exercise
    )


def get_user_test_statistics(user, exercise):
    tests = get_user_test_results(user, exercise)
    if tests:
        return (
            tests.exclude(test_count=0)
            .annotate(
                success_rate=Cast(F("success_count") * 100, FloatField())
                / Cast(F("test_count"), FloatField())
            )
            .values("success_rate", "test_count", "success_count")
            .order_by("-success_rate")[0]
        )
    else:
        return {
            "success_rate": 0,
            "test_count": 0,
            "success_count": 0,
        }
