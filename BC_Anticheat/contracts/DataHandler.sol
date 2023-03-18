// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "./ValidationRulesLib.sol";
import "./ValidationLib.sol";

contract DataHandler {
    mapping(string => int[]) int_data;
    mapping(string => string[]) string_data;
    mapping(
        string => ValidationRulesLib.IntValidationRule[]
    ) int_validation_rules;
    mapping(
        string => ValidationRulesLib.StringValidationRule[]
    ) string_validation_rules;

    function update_int_data(string memory key, int[] memory data) public {
        int_data[key] = data;
    }
    function update_string_data(string memory key, string[] memory data) public {
        string_data[key] = data;
    }
    function add_int_validation_rule(string memory key, int val, string memory operand) public {
        ValidationLib.validate_int_operand(operand);
        int_validation_rules[key].push(
            ValidationRulesLib.IntValidationRule({
                val: val, operand: operand
            })
        );
    }
    function add_string_validation_rule(string memory key, string memory val, string memory operand) public {
        ValidationLib.validate_string_operand(operand);
        string_validation_rules[key].push(
            ValidationRulesLib.StringValidationRule({
                val: val, operand: operand
            })
        );
    }

    function get_int_data(string memory key) public view returns (int[] memory) {
        // int[] memory data = int_data[key];
        // if (data.length == 0) {
        //     revert("Key DNE");
        // }
        // return data;
        return int_data[key];
    }
    function get_string_data(string memory key) public view returns (string[] memory) {
        // string[] memory data = string_data[key];
        // if (data.length == 0) {
        //     revert("Key DNE");
        // }
        // return data;
        return string_data[key];
    }
    function get_int_validation_rules(string memory key) public view
    returns (ValidationRulesLib.IntValidationRule[] memory) {
        return int_validation_rules[key];
    }
    function get_string_validation_rules(string memory key) public view
    returns (ValidationRulesLib.StringValidationRule[] memory) {
        return string_validation_rules[key];
    }
}
