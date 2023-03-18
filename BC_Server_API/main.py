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


@app.put("/session/{session_id}/data/{data_type}/{key}")
def put_session_data(
    session_id: str,
    data_type: Literal['int','str'],
    key: str,
    data: PutSessionData,
    response: Response
):
    """Put session data."""
    if data_type == 'int':
        success, msg = api.put_int_session_data(session_id, key, data.data) 
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
def get_session_data(session_id: str, data_type: Literal['int','str'], key: str, response: Response):
    """Get session data."""
    if data_type == 'int':
        success, msg = api.get_int_session_data(session_id, key) 
    elif data_type == 'str':
        success, msg = api.get_string_session_data(session_id, key)
    else:
        success, msg = False, 'Invalid data_type.'
    if success is False:
        response.status_code = 400
        return ErrorResponseModel(error=msg)
    return SuccessResponseModel(data=msg)


@app.get("/session/{session_id}/player/{player_id}/data/{data_type}/{key}")
def get_player_data(
    session_id: str,
    player_id: str,
    data_type: Literal['int','str'],
    key: str,
    response: Response
):
    """Get player data."""
    if data_type == 'int':
        success, msg = api.get_int_player_data(session_id, player_id, key) 
    elif data_type == 'str':
        success, msg = api.get_string_player_data(session_id, player_id, key)
    else:
        success, msg = False, 'Invalid data_type.'
    if success is False:
        response.status_code = 400
        return ErrorResponseModel(error=msg)
    return SuccessResponseModel(data=msg)


@app.put("/session/{session_id}/rule/{data_type}/{key}")
def put_session_data_validation_rule(
    session_id: str,
    data_type: Literal['int','str'],
    key: str,
    data: PutSessionDataValidationRule,
    response: Response
):
    """Update session data validation rule."""
    if data_type == 'int':
        success, msg = api.put_int_session_data_validation_rule(
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
    return SuccessResponseModel(data=msg)


@app.put("/session/{session_id}/data/{data_type}/{key}/validate")
def put_validate_and_update_session_data(
    session_id: str,
    data_type: Literal['int','str'],
    key: str,
    data: PutSessionData,
    response: Response
):
    """Put session data and validate."""
    if data_type == 'int':
        success, msg = api.put_validate_and_update_session_int_data(
            session_id, key, data.data
        )
    elif data_type == 'str':
        success, msg = api.put_validate_and_update_session_string_data(
            session_id, key, [str(x) for x in data.data]
        )
    else:
        success, msg = False, 'Invalid data_type.'
    if success is False:
        response.status_code = 400
        return ErrorResponseModel(error=msg)
    print(msg)
    return SuccessResponseModel(data=msg)


@app.put("/session/{session_id}/player/{player_id}/data/{data_type}/{key}/validate")
def put_validate_and_update_player_data(
    session_id: str,
    player_id: str,
    data_type: Literal['int','str'],
    key: str,
    data: PutSessionData,
    response: Response
):
    """Put session data and validate."""
    if data_type == 'int':
        success, msg = api.put_validate_and_update_player_int_data(
            session_id, player_id, key, data.data
        )
    elif data_type == 'str':
        success, msg = api.put_validate_and_update_player_string_data(
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
    data_type: Literal['int','str'],
    key: str,
    response: Response
):
    """Get session data validation rules."""
    if data_type == 'int':
        success, msg = api.get_session_data_int_validation_rules(session_id, key)
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
