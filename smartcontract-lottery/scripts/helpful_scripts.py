from brownie import accounts, network, config, MockV3Aggregator, VRFCoordinatorMock, Contract

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator, "vrf_coordinator": VRFCoordinatorMock}

def get_contract(contract_name):
    """
    This function will grab the contract address from brownie config if defined, otherwise
    it will deploy mock version of contract, and return that mock version

        Args:
            contract_name (string)
        
        Returns:
            brownie.network.contract.ProjectContract: the most recently deployed version
      
    
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # abi
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )


DECIMALS = 8
INITIAL_VALUE = 200000000000

def deploy_mocks():
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    print("Deployed!")
    
   