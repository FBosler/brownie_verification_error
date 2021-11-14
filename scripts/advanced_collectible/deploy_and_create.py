from scripts.helper import (
    fetch_from_active_network,
    get_account,
    get_contract,
    fund_with_link,
    OPENSEA_URL,
)
from brownie import AdvancedCollectible


def deploy_and_create():
    account = get_account()
    print(AdvancedCollectible.get_verification_info())
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        fetch_from_active_network("keyhash"),
        fetch_from_active_network("fee"),
        {"from": account},
        publish_source=True,
    )
    fund_with_link(
        advanced_collectible.address,
    )
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created!")


def main():
    deploy_and_create()
