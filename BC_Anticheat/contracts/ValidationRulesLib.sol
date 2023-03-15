// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

library ValidationRulesLib {
    struct SessionIntValidationRule {
        int val;
        string operand;
    }
    struct SessionBoolValidationRule {
        bool val;
        string operand;
    }
    struct SessionStringValidationRule {
        string val;
        string operand;
    }
}
