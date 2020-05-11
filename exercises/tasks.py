import uuid
from django.utils.encoding import force_str

import docker
from django.conf import settings
from rq import get_current_job

from exercises.config import (
    DOCKER_IMAGE,
    DOCKER_RUNNER_PATH,
    DOCKER_SECURITY_OPTIONS,
    DOCKER_SETUP_OPTIONS,
)
from exercises.models import TestResult, TestMessage

COMPUTE_ERROR = "Evaluierung fehlgeschlagen. Bitte benutze keine `print` statements in deiner Abgabe!"


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
    sep = str(uuid.uuid4())
    metasep = str(uuid.uuid4())
    client = docker.from_env()
    output = client.containers.run(
        DOCKER_IMAGE,
        f"python runner.py {metasep} {sep}",
        **DOCKER_SETUP_OPTIONS,
        **DOCKER_SECURITY_OPTIONS,
        volumes=volumes,
    )
    results = force_str(output).split(metasep)
    test_count = results[1].strip()
    errors = list(filter(None, results[2].split(sep)))
    failures = list(filter(None, results[3].split(sep)))

    test = TestResult.objects.create(
        job_id=job.id,
        submission=submission,
        test_count=test_count,
        success_count=int(test_count) - len(errors) - len(failures),
    )
    for error in errors:
        TestMessage.objects.create(test=test, message=error.strip(), kind="error")
    for failure in failures:
        TestMessage.objects.create(test=test, message=failure.strip(), kind="failure")
