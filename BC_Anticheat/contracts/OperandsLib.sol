// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

library OperandsLib {
    function compareStrings(string memory a, string memory b) public pure returns (bool) {
        return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
    }

    function validate_operand(string memory op) public pure {
        if (!compareStrings(op, "eq") ||
            !compareStrings(op, "ne") ||
            !compareStrings(op, "lt") ||
            !compareStrings(op, "gt") ||
            !compareStrings(op, "lte") ||
            !compareStrings(op, "gte")
        ) {
            revert("Invalid operand.");
        }
    }

    function validate_array_operand(string memory op) public pure {
        if (!compareStrings(op, "isin") ||
            !compareStrings(op, "nisin")
        ) {
            revert("Invalid operand.");
        }
    }
}
