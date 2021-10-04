// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TestContract is ERC721, Ownable {

    uint256 public constant MAX_SUPPLY = 4;
    uint256 public nextTokenId = 1;
    uint256 private tokenPrice = .001 ether;
    uint256 public constant MAX_PER_TX = 2;
    string public baseTokenURI;
    address payable private a1;
    bool public isSaleActive;

    constructor() public ERC721
    (
        "The Dudez", "DUDE"
    )
    {
        isSaleActive = false;
    }

    function setBaseURI(string memory baseURI) public onlyOwner {
        _setBaseURI(baseURI);
    }
    
    function mintDudez(uint256 quantity) 
        external 
        payable 
    {
        require(
            isSaleActive, "The sale is not active!");
        require(
            ((nextTokenId -1) + quantity) <= MAX_SUPPLY, "This would exceed max supply!");
        require(
            quantity <= MAX_PER_TX, "Can only mint 2 per tx");
        require(
            msg.value >= (tokenPrice*quantity), "Not enough ether sent!" );

        for (uint256 i; i < quantity; i++){
            _safeMint(msg.sender, nextTokenId);
            nextTokenId++;
        }

    }
    
    // testing setting addresses for withdraw, will become array
    function setAddresses(address payable a) public onlyOwner{
        a1 = a;
    }

    function setSale(bool sale) public onlyOwner{
        isSaleActive = sale;
    }
    
    // testing manual payment splitting before playing with library
    // establishing withdraws
    function withdraw() public payable onlyOwner {
        require(payable(a1).send(address(this).balance));
        //require(payable(a2).send(address(this).balance * 50/100));
    }
}