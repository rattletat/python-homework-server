from exercises.models import TestResult, TestMessage


def get_user_test_results(user, exercise, add_messages=False):
    tests = TestResult.objects.filter(
        submission__user=user, submission__exercise=exercise
    )
    if add_messages:
        for test in tests:
            test.errors = TestMessage.objects.filter(kind="error", test=test)
            test.failures = TestMessage.objects.filter(kind="failure", test=test)
    return tests
