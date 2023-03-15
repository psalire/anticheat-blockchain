// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
import "./Session.sol";

// struct Coordinates {
//     int x;
//     int y;
//     int z;
// }

contract Player {

    string public id;
    // Coordinates public coordinates;
    mapping(string => bool) player_bool_data;
    mapping(string => int) player_int_data;

    constructor(string memory assigned_id) {
        id = assigned_id;
        // coordinates.x = 0;
        // coordinates.y = 0;
        // coordinates.z = 0;
    }

    // function get_position() public view returns (Coordinates memory) {
    //     return coordinates;
    // }
    // function get_x() public view returns (int) {
    //     return coordinates.x;
    // }
    // function get_y() public view returns (int) {
    //     return coordinates.y;
    // }
    // function get_z() public view returns (int) {
    //     return coordinates.z;
    // }
    function get_player_bool_data(string memory key) public view returns (bool) {
        return player_bool_data[key];
    }
    function get_player_int_data(string memory key) public view returns (int) {
        return player_int_data[key];
    }
    function update_player_bool_data(string memory key, bool data) public {
        player_bool_data[key] = data;
    }
    function get_player_int_data(string memory key, int data) public {
        player_int_data[key] = data;
    }
    // function update_position(Coordinates memory c) public {
    //     coordinates = c;
    // }
    // function update_x(int x) public {
    //     coordinates.x = x;
    // }
    // function update_y(int y) public {
    //     coordinates.y = y;
    // }
    // function update_z(int z) public {
    //     coordinates.z = z;
    // }
}
