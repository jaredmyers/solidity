// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    
    using SafeMathChainlink for uint256;
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;
    
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }
    
    function fund() public payable {
        //uint256 minimumUSD = 1*10**18;
        //require(getConversionRate(msg.value) >= minimumUSD, "Spend more");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }
    
    //this is saying -- the functions that our defined in the interface we are using, are located at
    //that contract address
    function getVersion() public view returns (uint256){
        return priceFeed.version();
    }
    
    function getPrice() public view returns (uint256){
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer);
    } 
    
    function getConversionRate(uint256 ethAmount) public view returns (uint256){
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUSD = (ethPrice * ethAmount) / 100000000000000000;
        return ethAmountInUSD;
    }
    
    function getEntranceFee() public view returns (uint256){
        //minUSD
        uint256 minimumUSD = 1 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    function withdraw() payable public onlyOwner {
        msg.sender.transfer(address(this).balance);
        for (uint256 funderIndex=0; funderIndex < funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
        
    }
}