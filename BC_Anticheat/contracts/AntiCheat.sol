// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
import "./Session.sol";
import "./Player.sol";
import "./SessionHandler.sol";
import "./ValidationLib.sol";

contract AntiCheat {
    SessionHandler public session_handler;

    constructor() {
        session_handler = new SessionHandler();
    }

    function validate_and_update_session_int_data(
        string memory session_id,
        string memory key,
        int[] memory data
    ) public {
        Session session = Session(session_handler.get_session(session_id));
        if (!ValidationLib.validate_int(
            session.get_int_validation_rules(key), data)
        ) {
            session.stop();
            revert("Session flagged");
        }
        session.update_int_data(key, data);
    }

    function validate_and_update_session_string_data(
        string memory session_id,
        string memory key,
        string[] memory data
    ) public {
        Session session = Session(session_handler.get_session(session_id));
        if (!ValidationLib.validate_string(
            session.get_string_validation_rules(key), data)
        ) {
            session.stop();
            revert("Session flagged");
        }
        session.update_string_data(key, data);
    }

    function validate_and_update_player_int_data(
        string memory session_id,
        string memory player_id,
        string memory key,
        int[] memory data
    ) public {
        Session session = Session(session_handler.get_session(session_id));
        address player_addr = session_handler.get_player_in_session(session_id, player_id);
        if (!ValidationLib.validate_int(
            session.get_int_validation_rules(key), data)
        ) {
            session.remove_player(player_addr);
            revert("Player flagged");
        }
        Player(player_addr).update_int_data(key, data);
    }

    function validate_and_update_player_string_data(
        string memory session_id,
        string memory player_id,
        string memory key,
        string[] memory data
    ) public {
        Session session = Session(session_handler.get_session(session_id));
        address player_addr = session_handler.get_player_in_session(session_id, player_id);
        if (!ValidationLib.validate_string(
            session.get_string_validation_rules(key), data)
        ) {
            session.remove_player(player_addr);
            revert("Player flagged");
        }
        Player(player_addr).update_string_data(key, data);
    }

}
