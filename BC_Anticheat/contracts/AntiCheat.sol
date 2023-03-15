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
        string memory player_id,
        string memory key,
        int[] memory data
    ) public {
        Session session = Session(session_handler.get_session(session_id));
        Player player = Player(session_handler.get_player(player_id));
        if (!ValidationLib.validate_int(
            session.get_session_int_validation_rules(key), data)
        ) {
            session.remove_player(address(player));
            revert("Flagged");
        }
        session.update_session_int_data(key, data);
    }

    function validate_and_update_session_bool_data(
        string memory session_id,
        string memory player_id,
        string memory key,
        bool[] memory data
    ) public {
        Session session = Session(session_handler.get_session(session_id));
        Player player = Player(session_handler.get_player(player_id));
        if (!ValidationLib.validate_bool(
            session.get_session_bool_validation_rules(key), data)
        ) {
            session.remove_player(address(player));
            revert("Flagged");
        }
        session.update_session_bool_data(key, data);
    }

    function validate_and_update_session_string_data(
        string memory session_id,
        string memory player_id,
        string memory key,
        string[] memory data
    ) public {
        Session session = Session(session_handler.get_session(session_id));
        Player player = Player(session_handler.get_player(player_id));
        if (!session.is_player_active(address(player))) {
            revert("Inactive player");
        }
        if (!ValidationLib.validate_string(
            session.get_session_string_validation_rules(key), data)
        ) {
            session.remove_player(address(player));
            revert("Flagged");
        }
        session.update_session_string_data(key, data);
    }

}
