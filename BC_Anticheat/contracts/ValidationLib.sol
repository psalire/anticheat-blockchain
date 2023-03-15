// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "./ValidationRulesLib.sol";

library ValidationLib {
    function validate_int(
        ValidationRulesLib.SessionIntValidationRule[] memory rules,
        int[] memory data
    ) public pure returns (bool) {
        for (uint i=0; i < rules.length; i++) {
            ValidationRulesLib.SessionIntValidationRule memory rule = rules[i];
            bool op_nin = compareStrings(rule.operand, "nin");
            if (compareStrings(rule.operand, "in") || op_nin) {
                bool is_in = false;
                for (uint j=0; j < data.length; j++) {
                    if (data[j] == rule.val) {
                        is_in = true;
                        break;
                    }
                }
                if ((op_nin && !is_in) || (!op_nin && is_in)) {
                    return false;
                }
            }
            else {
                bool is_flagged = false;
                for (uint j=0; j < data.length; j++) {
                    if (compareStrings(rule.operand, "gt")) {
                        is_flagged = data[j] > rule.val;
                    }
                    else if (compareStrings(rule.operand, "lt")) {
                        is_flagged = data[j] < rule.val;
                    }
                    else if (compareStrings(rule.operand, "gte")) {
                        is_flagged = data[j] >= rule.val;
                    }
                    else if (compareStrings(rule.operand, "lte")) {
                        is_flagged = data[j] <= rule.val;
                    }
                    else if (compareStrings(rule.operand, "eq")) {
                        is_flagged = data[j] == rule.val;
                    }
                    else if (compareStrings(rule.operand, "ne")) {
                        is_flagged = data[j] != rule.val;
                    }
                    if (is_flagged) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    function validate_bool(
        ValidationRulesLib.SessionBoolValidationRule[] memory rules,
        bool[] memory data
    ) public pure returns (bool) {
        bool is_flagged = false;
        for (uint i=0; i < rules.length; i++) {
            ValidationRulesLib.SessionBoolValidationRule memory rule = rules[i];
            bool op_nin = compareStrings(rule.operand, "nin");
            if (compareStrings(rule.operand, "in") || op_nin) {
                bool is_in = false;
                for (uint j=0; j < data.length; j++) {
                    if (data[j] == rule.val) {
                        is_in = true;
                        break;
                    }
                }
                if ((op_nin && !is_in) || (!op_nin && is_in)) {
                    return false;
                }
            }
            else {
                for (uint j=0; j < data.length; j++) {
                    if (compareStrings(rule.operand, "eq")) {
                        is_flagged = data[j] == rule.val;
                    }
                    else if (compareStrings(rule.operand, "ne")) {
                        is_flagged = data[j] != rule.val;
                    }
                    if (is_flagged) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    function validate_string(
        ValidationRulesLib.SessionStringValidationRule[] memory rules,
        string[] memory data
    ) public pure returns (bool) {
        bool is_flagged = false;
        for (uint i=0; i < rules.length; i++) {
            ValidationRulesLib.SessionStringValidationRule memory rule = rules[i];
            bool op_nin = compareStrings(rule.operand, "nin");
            if (compareStrings(rule.operand, "in") || op_nin) {
                bool is_in = false;
                for (uint j=0; j < data.length; j++) {
                    if (compareStrings(data[j], rule.val)) {
                        is_in = true;
                        break;
                    }
                }
                if ((op_nin && !is_in) || (!op_nin && is_in)) {
                    return false;
                }
            }
            else {
                for (uint j=0; j < data.length; j++) {
                    if (compareStrings(rule.operand, "eq")) {
                        is_flagged = compareStrings(data[j], rule.val);
                    }
                    else if (compareStrings(rule.operand, "ne")) {
                        is_flagged = !compareStrings(data[j], rule.val);
                    }
                    if (is_flagged) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    function validate_int_operand(string memory op) public pure {
        if (!compareStrings(op, "eq") &&
            !compareStrings(op, "ne") &&
            !compareStrings(op, "lt") &&
            !compareStrings(op, "gt") &&
            !compareStrings(op, "lte") &&
            !compareStrings(op, "gte") &&
            !compareStrings(op, "in") &&
            !compareStrings(op, "nin")
        ) {
            revert("Invalid operand.");
        }
    }

    function validate_bool_operand(string memory op) public pure {
        if (!compareStrings(op, "eq") &&
            !compareStrings(op, "ne") &&
            !compareStrings(op, "in") &&
            !compareStrings(op, "nin")
        ) {
            revert("Invalid operand.");
        }
    }

    function validate_string_operand(string memory op) public pure {
        if (!compareStrings(op, "eq") &&
            !compareStrings(op, "ne") &&
            !compareStrings(op, "in") &&
            !compareStrings(op, "nin")
        ) {
            revert("Invalid operand.");
        }
    }

    function compareStrings(string memory a, string memory b) public pure returns (bool) {
        return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
    }
}
