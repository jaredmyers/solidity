// SPDX-License-Identifier: MIT

pragma solidity ^0.6.12;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract TestContract2 is ERC721 {


    constructor () public ERC721 ("The Dudez", "DUD"){
        uint256 maxTokenSupply = 4;
        uint256 nextTokenId = 1;

    }

}