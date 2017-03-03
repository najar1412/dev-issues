import pytest
import requests

from issues_api.packages import apifunc

# TODO: figure out how to mock database?
# TODO: it might be better to build a sqlite database to run tests on?

#
API = 'http://127.0.0.1:5050/issues/api'

"""test all api views"""

def test_if_api_is_running():
    pass


def test_api_entry():

    r = requests.get(API)
    assert r.status_code == 200


def test_issue():

    r = requests.get('{}{}'.format(API, '/issue'))
    assert r.status_code == 200


def test_issue_by_id():
    # TODO: test
    pass


def test_patch_issue():
    # TODO: test
    pass


def test_project():

    r = requests.get('{}{}'.format(API, '/project'))
    assert r.status_code == 200


def test_project_by_id():
    # TODO: test
    pass


def test_patch_project():
    # TODO: test
    pass


def test_delete_project():
    # TODO: test
    pass


def test_user():

    r = requests.get('{}{}'.format(API, '/user'))
    assert r.status_code == 200


def test_patch_user():
    # TODO: test
    pass


def test_delete_user():
    # TODO: test
    pass


def test_client():

    r = requests.get('{}{}'.format(API, '/client'))
    assert r.status_code == 200


def test_patch_client():
    # TODO: test
    pass


def test_delete_client():
    # TODO: test
    pass


def test_comment():

    r = requests.get('{}{}'.format(API, '/comment'))
    assert r.status_code == 200


def test_patch_comment():
    # TODO: test
    pass


def test_delete_comment():
    # TODO: test
    pass
