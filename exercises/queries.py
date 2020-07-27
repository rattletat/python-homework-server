from exercises.models import TestResult, Submission
from django.db.models import Max
from collections import defaultdict


def get_user_test_results(user, exercise):
    return TestResult.objects.filter(
        submission__user=user, submission__exercise=exercise
    )


def convert_points_to_grade(points):
    if 190 < points and points <= 200:
        return 1.0
    elif 180 < points and points <= 190:
        return 1.3
    elif 170 < points and points <= 180:
        return 1.7
    elif 160 < points and points <= 170:
        return 2.0
    elif 150 < points and points <= 160:
        return 2.3
    elif 140 < points and points <= 150:
        return 2.7
    elif 130 < points and points <= 140:
        return 3.0
    elif 120 < points and points <= 130:
        return 3.3
    elif 110 < points and points <= 120:
        return 3.7
    elif 100 < points and points <= 110:
        return 4.0
    else:
        return 5.0


def get_user_test_statistics(user, exercise):
    tests = get_user_test_results(user, exercise)
    if tests:
        result = (
            tests.exclude(test_count=0)
            .values("test_count", "success_count")
            .order_by("-success_count")[0]
        )
        # Set upper limit on maximal tests
        # (needed when amount of tests is changed afterwards)
        result["test_count"] = min(result["test_count"], exercise.max_tests)
        result["success_count"] = min(result["success_count"], exercise.max_tests)
        result["success_rate"] = (result["success_count"] * 100) / result[
            "test_count"
        ]
        return result
    else:
        return {
            "success_rate": 0,
            "test_count": exercise.max_tests,
            "success_count": 0,
        }


def get_current_statistics():
    """ Returns all non-null scores anonymized. """
    results = Submission.objects.values("user", "exercise").annotate(
        rating=Max("testresult__success_count")
    )
    final_result = defaultdict(int)
    for result in results:
        if result["rating"] and result["rating"] > 5:
            final_result[result["user"]] += result["rating"]
    return sorted(final_result.values())
