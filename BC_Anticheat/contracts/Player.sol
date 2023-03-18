// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
// import "./Session.sol";
import "./DataHandler.sol";

contract Player is DataHandler {

    string public id;

    constructor(string memory assigned_id) {
        id = assigned_id;
    }
}
