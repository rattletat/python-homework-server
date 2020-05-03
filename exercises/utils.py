import hashlib


def generate_sha1(file):
    sha = hashlib.sha1()
    file.seek(0)
    while(True):
        buf = file.read(104857600)
        if not buf:
            break
        sha.update(buf)
    sha1 = sha.hexdigest()
    file.seek(0)
    return sha1


def get_submission_dir(obj, _):
    return f"submission/test_user/{obj.exercise.number}/{obj.uploaded}.py"
