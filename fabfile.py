from contextlib import contextmanager
from fabric.api import cd, local, prefix, shell_env


VENV_PATH = '~/.virtualenvs/baseships'
PYTHON_PATH = '/usr/bin/python3.4'
SETTINGS_MODULE = 'baseships.settings'


def install():
    local('virtualenv -p {} {}'.format(PYTHON_PATH, VENV_PATH))

    with _venv():
        local('pip install -r requirements.txt')

        _django('makemigrations')
        _django('migrate')
        _django('loaddata base.json')


def runserver():
    with _venv():
        _django('runserver')


def testf(target):
    with _venv():
        _django('test functional_tests.{} -v 2'.format(target))


def _django(command):
    return local('python manage.py {}'.format(command))


@contextmanager
def _venv():
    with shell_env(DJANGO_SETTINGS_MODULE=SETTINGS_MODULE):
        with prefix('. %s/bin/activate' % VENV_PATH):
            yield
