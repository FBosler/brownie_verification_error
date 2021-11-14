// contracts/AdvancedCollectible.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import '@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol';
import '@openzeppelin/contracts/utils/Counters.sol';
import '@chainlink/contracts/src/v0.8/VRFConsumerBase.sol';

contract AdvancedCollectible is ERC721URIStorage, VRFConsumerBase {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    bytes32 public keyhash;
    uint256 public fee;

    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }

    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;

    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721('Doggie', 'DOG')
    {
        fee = _fee;
        keyhash = _keyhash;
    }

    function createCollectible()
        public
        returns (bytes32)
    {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
        return requestId;
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = _tokenIds.current();
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        address owner = requestIdToSender[requestId];
        _mint(owner, newTokenId);
        _tokenIds.increment();
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            'ERC721: caller is not owner nor approved'
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
