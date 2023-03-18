// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
// import "./Player.sol";
import "./DataHandler.sol";
// import "./ValidationLib.sol";
// import "./ValidationRulesLib.sol";

enum SessionState {Ready, Running, Stopped}
contract Session is DataHandler {
    enum PlayerState {Default, Removed, Active}

    string public id;
    mapping(address => PlayerState) player_states;
    SessionState session_state = SessionState.Ready;

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

    // function remove_player(address player_id) public {
    function remove_player(address player_addr) public {
        // address player_addr = owner_anticheat.get_player_in_session(id, player_id);
        // if (player_addr != address(0x0)) {
        //     revert("Player address does not exist.");
        // }
        if (player_states[player_addr] != PlayerState.Active) {
            revert("Player not Active");
        }
        player_states[player_addr] = PlayerState.Removed;
    }

    function get_player_state(address player_addr) public view returns (PlayerState) {
        if (player_addr == address(0x0)) {
            revert("Player DNE");
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
