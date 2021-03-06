import os
import uuid

import docker
from django.conf import settings
from django.utils.encoding import force_str
from rq import get_current_job

from exercises.config import (
    DOCKER_IMAGE,
    DOCKER_RUNNER_PATH,
    DOCKER_SECURITY_OPTIONS,
    DOCKER_SETUP_OPTIONS,
)

from .models import ExerciseResource, TestResult

TIMEOUT_ERROR = "Dein Programm hat zu lange gebraucht!"
NO_OUTPUT_ERROR = (
    "Dein Programm ist unerwartet beendet.\n"
    + "Bitte entferne die sys.exit().\n"
    + "Wenn das nicht hilft, kontaktiere den Support."
)
UNKNOWN_ERROR = (
    "Unerwarteter Fehler.\n"
    "Versuch bitte die print statements wegzulassen!\n"
    "Wenn das nicht hilft, kontaktiere den Support."
)


def compute_test_result(submission):
    job = get_current_job()

    submission_path = settings.BASE_DIR + submission.file.url
    tests_path = settings.BASE_DIR + submission.exercise.tests.url
    runner_path = settings.BASE_DIR + DOCKER_RUNNER_PATH

    volumes = {
        runner_path: {"bind": "/app/runner.py", "mode": "ro"},
        tests_path: {"bind": "/app/tests.py", "mode": "ro"},
        submission_path: {"bind": "/app/submission.py", "mode": "ro"},
    }
    resources = ExerciseResource.objects.filter(exercise=submission.exercise)
    for resource in resources:
        resource_path = settings.BASE_DIR + resource.file.url
        volumes[resource_path] = {
            "bind": "/app/" + os.path.basename(resource.file.name),
            "mode": "ro",
        }

    sep = str(uuid.uuid4())
    client = docker.from_env()
    try:
        container = client.containers.run(
            DOCKER_IMAGE,
            f"python runner.py {sep}",
            **DOCKER_SETUP_OPTIONS,
            **DOCKER_SECURITY_OPTIONS,
            volumes=volumes,
            detach=True,
        )
        container.wait(timeout=submission.exercise.timeout)
        output = container.logs()
        results = force_str(output).split(sep)
        container.remove(force=True)
    except Exception as e:
        TestResult.objects.create(
            job_id=job.id,
            submission=submission,
            test_count=submission.exercise.max_tests,
            success_count=0,
            first_error=TIMEOUT_ERROR + "\n" + str(e),
        )
    else:

        # TODO Why does sys.exit() produces no result?
        try:
            test_count = results[1]
            success_count = results[2]
            first_error = results[3]
            first_failure = results[4]
        except IndexError:
            test_count = submission.exercise.max_tests
            success_count = 0
            first_error = UNKNOWN_ERROR
            first_failure = ""

        if not results or not any(results):
            test_count = submission.exercise.max_tests
            success_count = 0
            first_error = NO_OUTPUT_ERROR
            first_failure = ""

        TestResult.objects.create(
            job_id=job.id,
            submission=submission,
            test_count=test_count,
            success_count=success_count,
            first_error=first_error,
            first_failure=first_failure,
        )
