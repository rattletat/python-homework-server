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
    DOCKER_TIMEOUT,
)
from exercises.models import TestResult, ExerciseResource

TIMEOUT_ERROR = "TimeoutError: Dein Programm hat zu lange gebraucht!"


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
        print("HALLO " + str(resource))
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
        container.wait(timeout=DOCKER_TIMEOUT)
        output = container.logs()
        results = force_str(output).split(sep)
        container.remove(force=True)
    except Exception as e:
        TestResult.objects.create(
            job_id=job.id,
            submission=submission,
            test_count=1,
            success_count=0,
            first_error=TIMEOUT_ERROR + "\n" + str(e),
        )
    else:

        test_count = results[1]
        success_count = results[2]
        first_error = results[3]
        first_failure = results[4]

        TestResult.objects.create(
            job_id=job.id,
            submission=submission,
            test_count=test_count,
            success_count=success_count,
            first_error=first_error,
            first_failure=first_failure,
        )
