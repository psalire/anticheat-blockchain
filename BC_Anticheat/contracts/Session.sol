// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
import "./Player.sol";
// import "./AntiCheat.sol";
// import "./OperandsLib.sol";
import "./ValidationLib.sol";
import "./ValidationRulesLib.sol";


enum SessionState {Ready, Running, Stopped}
contract Session {
    enum PlayerState {Default, Removed, Active}

    string public id;
    mapping(address => PlayerState) player_states;
    SessionState session_state = SessionState.Ready;
    mapping(string => bool[]) session_bool_data;
    mapping(string => int[]) session_int_data;
    mapping(string => string[]) session_string_data;
    mapping(
        string => ValidationRulesLib.SessionIntValidationRule[]
    ) session_int_validation_rules;
    mapping(
        string => ValidationRulesLib.SessionBoolValidationRule[]
    ) session_bool_validation_rules;
    mapping(
        string => ValidationRulesLib.SessionStringValidationRule[]
    ) session_string_validation_rules;

    constructor(string memory assigned_id) {
        id = assigned_id;
    }

    // function add_player(string memory player_id) public {
    function add_player(address player_addr) public {
        // Query anticheat if player exists
        // address player_addr = owner_anticheat.get_player(player_id);
        // if (player_addr != address(0x0)) {
        //     revert("Player address does not exist.");
        // }

        player_states[player_addr] = PlayerState.Active;
    }

    function get_session_bool_data(string memory key) public view returns (bool[] memory) {
        bool[] memory data = session_bool_data[key];
        if (data.length == 0) {
            revert("Requested key does not exist.");
        }
        return data;
    }
    function get_session_int_data(string memory key) public view returns (int[] memory) {
        int[] memory data = session_int_data[key];
        if (data.length == 0) {
            revert("Requested key does not exist.");
        }
        return data;
    }
    function get_session_string_data(string memory key) public view returns (string[] memory) {
        string[] memory data = session_string_data[key];
        if (data.length == 0) {
            revert("Requested key does not exist.");
        }
        return data;
    }
    function update_session_data(
        string memory int_key,
        string memory bool_key,
        string memory string_key,
        int[] memory int_data,
        bool[] memory bool_data,
        string[] memory string_data
    ) public {
        update_session_int_data(int_key, int_data);
        update_session_bool_data(bool_key, bool_data);
        update_session_string_data(string_key, string_data);
    }
    function update_session_int_data(string memory key, int[] memory data) public {
        session_int_data[key] = data;
    }
    function update_session_bool_data(string memory key, bool[] memory data) public {
        session_bool_data[key] = data;
    }
    function update_session_string_data(string memory key, string[] memory data) public {
        session_string_data[key] = data;
    }

    function add_session_int_validation_rule(string memory key, int val, string memory operand) public {
        ValidationLib.validate_int_operand(operand);
        session_int_validation_rules[key].push(
            ValidationRulesLib.SessionIntValidationRule({
                val: val, operand: operand
            })
        );
    }
    function add_session_bool_validation_rule(string memory key, bool val, string memory operand) public {
        ValidationLib.validate_bool_operand(operand);
        session_bool_validation_rules[key].push(
            ValidationRulesLib.SessionBoolValidationRule({
                val: val, operand: operand
            })
        );
    }
    function add_session_string_validation_rule(string memory key, string memory val, string memory operand) public {
        ValidationLib.validate_string_operand(operand);
        session_string_validation_rules[key].push(
            ValidationRulesLib.SessionStringValidationRule({
                val: val, operand: operand
            })
        );
    }

    function get_session_int_validation_rules(string memory key) public view
    returns (ValidationRulesLib.SessionIntValidationRule[] memory) {
        return session_int_validation_rules[key];
    }
    function get_session_bool_validation_rules(string memory key) public view
    returns (ValidationRulesLib.SessionBoolValidationRule[] memory) {
        return session_bool_validation_rules[key];
    }
    function get_session_string_validation_rules(string memory key) public view
    returns (ValidationRulesLib.SessionStringValidationRule[] memory) {
        return session_string_validation_rules[key];
    }

    // function remove_player(address player_id) public {
    function remove_player(address player_addr) public {
        // address player_addr = owner_anticheat.get_player_in_session(id, player_id);
        // if (player_addr != address(0x0)) {
        //     revert("Player address does not exist.");
        // }
        if (player_states[player_addr] != PlayerState.Active) {
            revert("Player is not Active.");
        }
        player_states[player_addr] = PlayerState.Removed;
    }

    function get_player_state(address player_addr) public view returns (PlayerState) {
        if (player_addr == address(0x0)) {
            revert("Player address does not exist.");
        }
        return player_states[player_addr];
    }

    function is_player_active(address player_addr) public view returns(bool) {
        return get_player_state(player_addr) == PlayerState.Active;
    }

    function start() public {
        session_state = SessionState.Running;
    }

    function stop() public {
        session_state = SessionState.Stopped;
    }

    function is_running() public view returns (bool) {
        return session_state == SessionState.Running;
    }
}
