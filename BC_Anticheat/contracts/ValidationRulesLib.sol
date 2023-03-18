// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

library ValidationRulesLib {
    struct IntValidationRule {
        int val;
        string operand;
    }
    struct StringValidationRule {
        string val;
        string operand;
    }
}
