from brownie import network, accounts, config, Contract
from brownie import VRFCoordinatorMock, LinkToken
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200_000_000

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

is_local_fork = lambda: network.show_active() in FORKED_LOCAL_ENVIRONMENTS
is_dev = lambda: network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS


def fetch_from_active_network(key):
    return config["networks"][network.show_active()][key]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if is_dev() or is_local_fork():
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.

        Args:
            contract_name (string)

        Returns:
            bronwie.network.contract.ProjectContract: The most recently deployed
            version of this contract.

    """
    contract_type = contract_to_mock[contract_name]
    if is_dev():
        if len(contract_type) == 0:
            deploy_or_get_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract


def deploy_or_get_mocks():
    account = get_account()
    print(f"The active networks is {network.show_active()}")
    print(f"Deploying Mocks ....")
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, "ether")
):  # 0.1 Link
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Funded contract")
    return tx
