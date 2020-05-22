import hashlib
import os


def generate_sha1(file):
    sha = hashlib.sha1()
    file.seek(0)
    while True:
        buf = file.read(104857600)
        if not buf:
            break
        sha.update(buf)
    sha1 = sha.hexdigest()
    file.seek(0)
    return sha1


def get_submission_path(obj, _):
    return os.path.join(
        "submissions", str(obj.user.uid), str(obj.exercise.number), f"{obj.uploaded}.py",
    )


def get_description_path(obj, _):
    return os.path.join("exercises", str(obj.number), "description.md")


def get_tests_path(obj, _=None):
    return os.path.join("exercises", str(obj.number), "tests.py")


def get_resources_path(obj, filename):
    return os.path.join("exercises", str(obj.exercise.number), "rsc", filename)
