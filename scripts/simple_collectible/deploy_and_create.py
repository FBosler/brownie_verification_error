from scripts.helper import get_account, OPENSEA_URL
from brownie import SimpleCollectible


sample_token_uri = (
    "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
)
sample_token_uri = "https://ipfs.io/ipfs/bafkreihsxjsj7fyw2sfmznaobdpmn2onkxbkqguuohzhouixkvupwotlcm?filename=sunset.json"


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy(
        {"from": account},
        # publish_source = True
    )
    tx = simple_collectible.awardItem(account.address, sample_token_uri, {"from": account})
    tx.wait(1)
    addr = simple_collectible.address
    print(tx.events["Transfer"])
    token_id = tx.events["Transfer"][-1]["tokenId"]
    print(f"Awesome, you can view your NFT at {OPENSEA_URL.format(addr, token_id)}")
    return simple_collectible


def main():
    deploy_and_create()
