
from scripts.helpful_scripts import get_account
from brownie import TestContract

def deploy_and_create():
    account = get_account()
    test_contract = TestContract.deploy({"from": account}, publish_source=True)
    print("Awsome, you can not view your NFT")

    

def main():
    deploy_and_create()