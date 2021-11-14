### Description
Getting a verification error when running `brownie run scripts/advanced_collectible/deploy_and_create.py --network rinkeby` even though the contract seems to be working
![image](https://user-images.githubusercontent.com/14016698/141688780-339330f3-9109-4d7a-889e-ad371e1d186b.png)


### To replicate
- `pip install -r requirements.txt` (there might be some leftovers from another project, `pip insall eth-brownie py-solc-x web3` might also do it)
- `brownie compile`
- `create and fill out .env file`
- `make sure you have enough LINK and ETH on Rinkeby -> https://faucets.chain.link/rinkeby`
- `brownie run scripts/advanced_collectible/deploy_and_create.py --network rinkeby`
- `deployment works, verification fails'


### Note
This project is far from finished or funtional.
