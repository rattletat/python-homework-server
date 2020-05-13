from exercises.models import TestResult


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
        result["success_count"] = min(
            result["success_count"], exercise.max_tests
        )
        result["success_rate"] = result["success_count"] / result["test_count"]
        return result
    else:
        return {
            "success_rate": 0,
            "test_count": exercise.max_tests,
            "success_count": 0,
        }
