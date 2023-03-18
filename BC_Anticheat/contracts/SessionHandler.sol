// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "./Session.sol";
import "./Player.sol";

contract SessionHandler {
    mapping(string => address) game_sessions;
    mapping(string => address) players;

    function add_new_session(string memory session_id) public {
        // Check for duplicates
        require(game_sessions[session_id] == address(0x0));

        Session new_session = new Session(session_id);
        game_sessions[session_id] = address(new_session);
    }

    function add_new_player(string memory session_id, string memory player_id) public {
        // Check for duplicates
        require(players[player_id] == address(0x0));

        Session session = Session(get_session(session_id));
        Player new_player = new Player(player_id);
        players[player_id] = address(new_player);
        session.add_player(address(new_player));
    }

    function get_player(string memory player_id) public view returns (address) {
        address player_addr = players[player_id];
        if (player_addr == address(0x0)) {
            revert("Player DNE");
        }
        return player_addr;
    }

    function get_player_in_session(string memory session_id, string memory player_id) public view returns (address) {
        Session session = Session(get_session(session_id));
        address player_addr = players[player_id];
        if (!session.is_player_active(player_addr)) {
            revert("Player not Active");
        }
        return player_addr;
    }

    function get_session(string memory session_id) public view returns (address) {
        address session_addr = game_sessions[session_id];
        if (session_addr == address(0x0)) {
            revert("Session DNE");
        }
        return session_addr;
    }
}
