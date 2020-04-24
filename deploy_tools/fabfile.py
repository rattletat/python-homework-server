import random
from fabric.contrib.files import append, exists
from fabric.api import cd, sudo, env, local, run

REPO_URL = 'https://github.com/rattletat/homework-server.git'

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    poetry_installed = run("poetry about").failed
    if not poetry_installed:
        run("curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python")
        run('source $HOME/.poetry/env')
        sudo("apt get install python3.8 -y")
        sudo("apt get install python3-pip -y")
        sudo("apt get install python3.8-venv -y")
    if not exists('pyproject.toml'):
        run(f'poetry new . -n --src --name {env.host}')
    run('poetry install')


def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEPLOY=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        choices = 'abcdefghijklmnopqrstuvwxyz123456789'
        new_secret = ''.join(random.SystemRandom().choices(choices, k=50))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')


def _update_static_files():
    run('poetry run python3.8 manage.py collectstatic --noinput')


def _update_database():
    run('poetry run python3.8 manage.py migrate --noinput')
