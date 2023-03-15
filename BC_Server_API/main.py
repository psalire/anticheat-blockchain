"""Anti-cheat blockchain Server API."""
from uuid import uuid4
from W3Facade import W3Facade
from fastapi import FastAPI, Response
from typing import Literal
from ResponseModels import SuccessResponseModel, ErrorResponseModel
from RequestModels import PutSessionData, PutSessionDataBatch, PutSessionDataValidationRule

app = FastAPI()

# Initialize Web3 interface to contract
api = W3Facade('http://127.0.0.1:7545')


@app.get("/version")
def get_version():
    """Get API version number."""
    return SuccessResponseModel(
        data={
            "version": "1.0"
        }
    )


@app.post("/session/{session_id}", status_code=201)
def post_session(session_id: str, response: Response):
    """Create a new game session and return its ID."""
    success, msg = api.add_session(session_id)
    if not success:
        response.status_code = 400
        return ErrorResponseModel(error=msg)

    return SuccessResponseModel(
        data={
            "session_id": session_id,
        }
    )


@app.post("/session", status_code=201)
def post_session_random_uuid(response: Response):
    """Create a new game session with UUID and return its ID."""
    session_id = str(uuid4())
    success, msg = api.add_session(session_id)
    if not success:
        response.status_code = 400
        return ErrorResponseModel(error=msg)

    return SuccessResponseModel(
        data={
            "session_id": session_id,
        }
    )


@app.get("/session/{session_id}")
def get_session(session_id: str, response: Response):
    """Get an existing session."""
    success, msg = api.get_session(session_id=session_id)
    if success is False or not msg:
        response.status_code = 400
        return ErrorResponseModel(error=msg)

    return SuccessResponseModel(
        data={
            "session_id": session_id,
            "address": msg.address,
        }
    )


@app.post("/session/{session_id}/player/{player_id}", status_code=201)
def post_player_to_session(session_id: str, player_id: str, response: Response):
    """Add a player to a session."""
    success, msg = api.add_player_to_session(session_id, player_id)
    if success is False:
        response.status_code = 400
        return ErrorResponseModel(
            error=msg
        )

    return SuccessResponseModel(
        data={
            "session_id": session_id,
            "player_id": player_id,
        }
    )


# @app.put("/session/{session_id}/player/{player_id}")
# def put_player_position_to_session(
#     request_body: PostPlayerPositionRequest, session_id: str, player_id: str, response: Response
# ):
#     """Update player position."""
#     success, msg = api.validate_and_update_player_position(
#         session_id,
#         player_id,
#         request_body.coordinates.x,
#         request_body.coordinates.y,
#         request_body.coordinates.z,
#     )
#     if success is False:
#         response.status_code = 400
#         return ErrorResponseModel(
#             error=msg
#         )

#     return SuccessResponseModel(
#         data={
#             "session_id": session_id,
#             "player_id": player_id,
#             "coordinates": {
#                 "x": request_body.coordinates.x,
#                 "y": request_body.coordinates.y,
#                 "z": request_body.coordinates.z
#             }
#         }
#     )


# @app.post("/session/{session_id}/validation_rule/position")
# def post_position_validation_rule(
#     request_body: PostPositionValidationRule,
#     session_id: str,
#     response: Response
# ):
#     """Add new position validation rule to session."""
#     success, msg = api.add_position_validation_rule(
#         session_id,
#         request_body.rule.operand,
#         request_body.rule.coordinates.x,
#         request_body.rule.coordinates.y,
#         request_body.rule.coordinates.z,
#     )
#     if success is False:
#         response.status_code = 400
#         return ErrorResponseModel(error=msg)
#     return SuccessResponseModel(
#         data={
#             "session_id": session_id,
#             "rule": {
#                 "operand": request_body.rule.operand,
#                 "x": request_body.rule.coordinates.x,
#                 "y": request_body.rule.coordinates.y,
#                 "z": request_body.rule.coordinates.z,
#             }
#         }
#     )


@app.put("/session/{session_id}/data")
def put_session_data_batch(session_id: str, data: PutSessionDataBatch, response: Response):
    """Update session data."""
    int_key = data.int_key if data.int_key else ""
    bool_key = data.bool_key if data.bool_key else ""
    string_key = data.string_key if data.string_key else ""
    success, msg = api.update_session_data(
        session_id,
        int_key, bool_key, string_key,
        data.int_data, data.bool_data, data.string_data
    )
    if success is False:
        response.status_code = 400
        return ErrorResponseModel(error=msg)
    return SuccessResponseModel(data=msg)


@app.put("/session/{session_id}/data/{data_type}/{key}")
def put_session_data(
    session_id: str,
    data_type: Literal['int','bool','str'],
    key: str,
    data: PutSessionData,
    response: Response
):
    """Put session data."""
    if data_type == 'int':
        success, msg = api.put_int_session_data(session_id, key, data.data) 
    elif data_type == 'bool':
        success, msg = api.put_bool_session_data(session_id, key, data.data)
    elif data_type == 'str':
        success, msg = api.put_string_session_data(session_id, key, data.data)
    else:
        success, msg = False, 'Invalid data_type.'
    if success is False:
        response.status_code = 400
        return ErrorResponseModel(error=msg)
    print(msg)
    return SuccessResponseModel(data=msg)


@app.get("/session/{session_id}/data/{data_type}/{key}")
def get_session_data(session_id: str, data_type:  Literal['int','bool','str'], key: str, response: Response):
    """Get session data."""
    if data_type == 'int':
        success, msg = api.get_int_session_data(session_id, key) 
    elif data_type == 'bool':
        success, msg = api.get_bool_session_data(session_id, key)
    elif data_type == 'str':
        success, msg = api.get_string_session_data(session_id, key)
    else:
        success, msg = False, 'Invalid data_type.'
    if success is False:
        response.status_code = 400
        return ErrorResponseModel(error=msg)
    return SuccessResponseModel(data=msg)


@app.put("/session/{session_id}/rule/{data_type}/{key}")
def put_session_data_validation_rule(
    session_id: str,
    data_type: Literal['int','bool','str'],
    key: str,
    data: PutSessionDataValidationRule,
    response: Response
):
    """Update session data validation rule."""
    if data_type == 'int':
        success, msg = api.put_int_session_data_validation_rule(
            session_id, key, data.data, data.operand
        ) 
    elif data_type == 'bool':
        success, msg = api.put_bool_session_data_validation_rule(
            session_id, key, data.data, data.operand
        )
    elif data_type == 'str':
        success, msg = api.put_string_session_data_validation_rule(
            session_id, key, str(data.data), data.operand
        )
    else:
        success, msg = False, 'Invalid data_type.'
    if success is False:
        response.status_code = 400
        return ErrorResponseModel(error=msg)
    print(msg)
    return SuccessResponseModel(data=msg)


@app.put("/session/{session_id}/data/{data_type}/{key}/validate/player/{player_id}")
def put_validate_and_update_session_data(
    session_id: str,
    player_id: str,
    data_type: Literal['int','bool','str'],
    key: str,
    data: PutSessionData,
    response: Response
):
    """Put session data and validate."""
    if data_type == 'int':
        success, msg = api.put_validate_and_update_session_int_data(
            session_id, player_id, key, data.data
        )
    elif data_type == 'bool':
        success, msg = api.put_validate_and_update_session_bool_data(
            session_id, player_id, key, data.data
        )
    elif data_type == 'str':
        success, msg = api.put_validate_and_update_session_string_data(
            session_id, player_id, key, [str(x) for x in data.data]
        )
    else:
        success, msg = False, 'Invalid data_type.'
    if success is False:
        response.status_code = 400
        return ErrorResponseModel(error=msg)
    print(msg)
    return SuccessResponseModel(data=msg)


@app.get("/session/{session_id}/rule/{data_type}/{key}")
def get_session_data_validation_rules(
    session_id: str,
    data_type: Literal['int', 'bool', 'str'],
    key: str,
    response: Response
):
    """Get session data validation rules."""
    if data_type == 'int':
        success, msg = api.get_session_data_int_validation_rules(session_id, key)
    elif data_type == 'bool':
        success, msg = api.get_session_data_bool_validation_rules(session_id, key)
    elif data_type == 'str':
        success, msg = api.get_session_data_string_validation_rules(session_id, key)
    else:
        success, msg = False, 'Invalid data_type.'
    if success is False:
        response.status_code = 400
        return ErrorResponseModel(error=msg)
    return SuccessResponseModel(data=[{
        'val': x[0],
        'operand': x[1]
    } for x in msg])


# @app.put("/session/{session_id}/rule")
# def put_session_validation_rule(session_id: str, rule: PutSessionValidationRule, response: Response):
#     """Put session validation rule."""
#     int_key = rule.int_key if rule.int_key else ""
#     bool_key = rule.bool_key if rule.bool_key else ""
#     string_key = rule.string_key if rule.string_key else ""
#     success, msg = api.add_session_data_validation_rule(
#         session_id,
#         int_key, bool_key, string_key,
#         rule.ints, rule.bools, rule.strings,
#         rule.int_operands, rule.bool_operands, rule.string_operands,
#     )
#     if success is False:
#         response.status_code = 400
#         return ErrorResponseModel(error=msg)
#     return SuccessResponseModel(data=msg)


# @app.get("/session/{session_id}/rules")
# def get_session_validation_rules(session_id: str, response: Response):
#     """Get session validation rules."""
#     success, msg = api.get_session_validation_rules(session_id)
#     if success is False:
#         response.status_code = 400
#         return ErrorResponseModel(error=msg)
#     return SuccessResponseModel(data=[{
#         'int_key': x[0],
#         'bool_key': x[1],
#         'string_key': x[2],
#         'ints': x[3],
#         'bools': x[4],
#         'strings': x[5],
#         'int_operands': x[6],
#         'bool_operands': x[7],
#         'string_operands': x[8],
#     } for x in msg])


# @app.get("/session/{session_id}/validation_rule/position/all")
# def get_position_validation_rules(session_id: str, response: Response):
#     """Get position validation rules list."""
#     success, msg = api.get_position_validation_rules(session_id)
#     if success is False:
#         response.status_code = 400
#         return ErrorResponseModel(error=msg)
#     return SuccessResponseModel(
#         data={
#             "position_validation_rules": msg
#         }
#     )


@app.get("/player/{player_id}")
def get_player(player_id: str, response: Response):
    """Get Player address."""
    success, msg = api.get_player(player_id)
    if success is False or not msg:
        response.status_code = 400
        return ErrorResponseModel(error=msg)

    return SuccessResponseModel(
        data={
            "player_id": player_id,
            "address": msg.address,
        }
    )


# @app.get("/session/{session_id}/player/{player_id}/position")
# def get_player_position(session_id: str, player_id: str, response: Response):
#     """Get Player position."""
#     success, msg = api.get_player_position(session_id, player_id)
#     if success is False or not msg:
#         response.status_code = 400
#         return ErrorResponseModel(error=msg)

#     return SuccessResponseModel(
#         data={
#             "position": {
#                 'x': msg[0],
#                 'y': msg[1],
#                 'z': msg[2]
#             }
#         }
#     )
