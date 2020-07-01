from exercises.models import TestResult, Submission
from django.db.models import Max
from collections import defaultdict


def get_user_test_results(user, exercise):
    return TestResult.objects.filter(
        submission__user=user, submission__exercise=exercise
    )


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
        if result['rating'] and result['rating'] > 5:
            final_result[result['user']] += result['rating']
    return sorted(final_result.values())
