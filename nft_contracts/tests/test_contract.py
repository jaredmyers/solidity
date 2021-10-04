from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network
import pytest
from scripts.deploy_and_create import deploy_and_create

def test_can_mint_dudez():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    test_contract = deploy_and_create()
    assert test_contract.ownerOf(0) == get_account()