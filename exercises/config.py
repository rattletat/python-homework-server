import os


# === DOCKER OPTIONS ===

DOCKER_IMAGE = "python:3"
DOCKER_WORKING_DIR = "/app"
DOCKER_SETUP_OPTIONS = {
    "auto_remove": True,
    "working_dir": DOCKER_WORKING_DIR,
}
DOCKER_SECURITY_OPTIONS = {
    "user": "1000:1000",
    "read_only": True,
    "network_disabled": True,
    "network_mode": "none",
    "mem_limit": "1g",
    "cap_drop": ["ALL"],
}
DOCKER_RUNNER_PATH = os.path.join("/exercises", "utils", "runner.py")
