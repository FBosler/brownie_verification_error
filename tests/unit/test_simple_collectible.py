from scripts.helper import is_dev, is_local_fork, get_account
from scripts.deploy_and_create import deploy_and_create
import pytest


def test_can_create_simple_collectible():
    # skip tests if its not a local fork
    if not is_local_fork():
        pytest.skip()
    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf(1) == get_account()
