import os
import pytest

from Movie_Web_App import create_app
from Movie_Web_App.adapters import memory_repository
from Movie_Web_App.adapters.memory_repository import MemoryRepository


TEST_DATA_PATH = os.path.join('tests', 'data')
#TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'iwar006', 'Documents', 'Python dev', 'COVID-19', 'tests', 'data')


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='thorke', password='cLQ^C#oFXloS'):
        return self._client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)