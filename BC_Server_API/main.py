"""Anti-cheat blockchain Server API."""
from uuid import uuid4
from W3Facade import W3Facade
from fastapi import FastAPI, Response, WebSocket
from fastapi.responses import HTMLResponse
from typing import Literal
from ResponseModels import SuccessResponseModel, ErrorResponseModel
from RequestModels import PutSessionData, PutSessionDataValidationRule, WSRequest
import json

app = FastAPI()

# Initialize Web3 interface to contract
api = W3Facade('http://127.0.0.1:7545')

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <textarea type="text" id="messageText" autocomplete="off"></textarea>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    fun = lambda: ErrorResponseModel(error="Unexpected error")
    while True:
        try:
            text = await websocket.receive_text()
            if text:
                data = json.loads(text)
                ws_req = WSRequest(
                    action=data['action'],
                    msg=data['msg'] if 'msg' in data else None
                )
                if ws_req.action == 'version':
                    fun = get_version
                elif ws_req.action == 'post_session':
                    fun = lambda: post_session(
                        ws_req.msg['session_id'],
                    )
                elif ws_req.action == 'post_session_random':
                    fun = lambda: post_session_random_uuid()
                elif ws_req.action == 'get_session':
                    fun = lambda: get_session(
                        ws_req.msg['session_id'],
                    )
                elif ws_req.action == 'post_player_to_session':
                    fun = lambda: post_player_to_session(
                        ws_req.msg['session_id'],
                        ws_req.msg['player_id'],
                    )
                elif ws_req.action == 'post_player_to_session_random':
                    fun = lambda: post_player_to_session_random(
                        ws_req.msg['session_id'],
                    )
                elif ws_req.action == 'put_session_data':
                    fun = lambda: put_session_data(
                        ws_req.msg['session_id'],
                        ws_req.msg['data_type'],
                        ws_req.msg['key'],
                        PutSessionData(data=ws_req['data']),
                    )
                elif ws_req.action == 'get_session_data':
                    fun = lambda: get_session_data(
                        ws_req.msg['session_id'],
                        ws_req.msg['data_type'],
                        ws_req.msg['key'],
                    )
                elif ws_req.action == 'get_player_data':
                    fun = lambda: get_player_data(
                        ws_req.msg['session_id'],
                        ws_req.msg['player_id'],
                        ws_req.msg['data_type'],
                        ws_req.msg['key'],
                    )
                elif ws_req.action == 'put_session_data_validation_rule':
                    fun = lambda: put_session_data_validation_rule(
                        ws_req.msg['session_id'],
                        ws_req.msg['data_type'],
                        ws_req.msg['key'],
                    )
                elif ws_req.action == 'put_validate_and_update_session_data':
                    fun = lambda: put_validate_and_update_session_data(
                        ws_req.msg['session_id'],
                        ws_req.msg['data_type'],
                        ws_req.msg['key'],
                        PutSessionData(ws_req.msg['data']),
                    )
                elif ws_req.action == 'put_validate_and_update_player_data':
                    fun = lambda: put_validate_and_update_player_data(
                        ws_req.msg['session_id'],
                        ws_req.msg['player_id'],
                        ws_req.msg['data_type'],
                        ws_req.msg['key'],
                        PutSessionData(ws_req.msg['data']),
                    )
                elif ws_req.action == 'get_session_data_validation_rules':
                    fun = lambda: get_session_data_validation_rules(
                        ws_req.msg['session_id'],
                        ws_req.msg['data_type'],
                        ws_req.msg['key'],
                        PutSessionData(ws_req.msg['data']),
                    )
                elif ws_req.action == 'get_player':
                    fun = lambda: get_player(
                        ws_req.msg['player_id'],
                    )
                else:
                    fun = lambda: ErrorResponseModel(error="Unknown action")
            else:
                fun = lambda: ErrorResponseModel(error="Invalid input")
        except Exception as err:
            print(err)
            fun = lambda: ErrorResponseModel(error="Exception")
        if fun:
            await websocket.send_json(
                dict(fun())
            )


@app.websocket("/session/{session_id}")
async def ws_post_session(websocket: WebSocket, session_id: str):
    await websocket.accept()
    await websocket.send_json(
        dict(post_session(session_id, None))
    )


@app.get("/version")
def get_version():
    """Get API version number."""
    return SuccessResponseModel(
        data={
            "version": "1.0"
        }
    )


@app.post("/session/{session_id}", status_code=201)
def post_session(session_id: str, response: Response=None):
    """Create a new game session and return its ID."""
    success, msg = api.add_session(session_id)
    if not success:
        if response:
            response.status_code = 400
        return ErrorResponseModel(error=msg)

    return SuccessResponseModel(data=msg)


@app.post("/session", status_code=201)
def post_session_random_uuid(response: Response=None):
    """Create a new game session with UUID and return its ID."""
    session_id = str(uuid4())
    success, msg = api.add_session(session_id)
    if not success:
        if response:
            response.status_code = 400
        return ErrorResponseModel(error=msg)

    return SuccessResponseModel(data={
        'session_id': session_id
    })


@app.get("/session/{session_id}")
def get_session(session_id: str, response: Response=None):
    """Get an existing session."""
    success, msg = api.get_session(session_id=session_id)
    if success is False or not msg:
        if response:
            response.status_code = 400
        return ErrorResponseModel(error=msg)

    return SuccessResponseModel(
        data={
            "address": msg.address,
        }
    )


@app.post("/session/{session_id}/player/{player_id}", status_code=201)
def post_player_to_session(session_id: str, player_id: str, response: Response=None):
    """Add a player to a session."""
    success, msg = api.add_player_to_session(session_id, player_id)
    if success is False:
        if response:
            response.status_code = 400
        return ErrorResponseModel(
            error=msg
        )

    return SuccessResponseModel(data=msg)


@app.post("/session/{session_id}/player", status_code=201)
def post_player_to_session_random(session_id: str, response: Response=None):
    """Add a player to a session with UUID."""
    player_id = str(uuid4())
    success, msg = api.add_player_to_session(session_id, player_id)
    if success is False:
        if response:
            response.status_code = 400
        return ErrorResponseModel(
            error=msg
        )

    return SuccessResponseModel(data=msg)


@app.put("/session/{session_id}/data/{data_type}/{key}")
def put_session_data(
    session_id: str,
    data_type: Literal['int','str'],
    key: str,
    data: PutSessionData,
    response: Response=None
):
    """Put session data."""
    if data_type == 'int':
        success, msg = api.put_int_session_data(session_id, key, data.data) 
    elif data_type == 'str':
        success, msg = api.put_string_session_data(session_id, key, data.data)
    else:
        success, msg = False, 'Invalid data_type.'
    if success is False:
        if response:
            response.status_code = 400
        return ErrorResponseModel(error=msg)
    return SuccessResponseModel(data=msg)


@app.get("/session/{session_id}/data/{data_type}/{key}")
def get_session_data(session_id: str, data_type: Literal['int','str'], key: str, response: Response=None):
    """Get session data."""
    if data_type == 'int':
        success, msg = api.get_int_session_data(session_id, key) 
    elif data_type == 'str':
        success, msg = api.get_string_session_data(session_id, key)
    else:
        success, msg = False, 'Invalid data_type.'
    if success is False:
        if response:
            response.status_code = 400
        return ErrorResponseModel(error=msg)
    return SuccessResponseModel(data=msg)


@app.get("/session/{session_id}/player/{player_id}/data/{data_type}/{key}")
def get_player_data(
    session_id: str,
    player_id: str,
    data_type: Literal['int','str'],
    key: str,
    response: Response=None
):
    """Get player data."""
    if data_type == 'int':
        success, msg = api.get_int_player_data(session_id, player_id, key) 
    elif data_type == 'str':
        success, msg = api.get_string_player_data(session_id, player_id, key)
    else:
        success, msg = False, 'Invalid data_type.'
    if success is False:
        if response:
            response.status_code = 400
        return ErrorResponseModel(error=msg)
    return SuccessResponseModel(data=msg)


@app.put("/session/{session_id}/rule/{data_type}/{key}")
def put_session_data_validation_rule(
    session_id: str,
    data_type: Literal['int','str'],
    key: str,
    data: PutSessionDataValidationRule,
    response: Response=None
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
        if response:
            response.status_code = 400
        return ErrorResponseModel(error=msg)
    return SuccessResponseModel(data=msg)


@app.put("/session/{session_id}/data/{data_type}/{key}/validate")
def put_validate_and_update_session_data(
    session_id: str,
    data_type: Literal['int','str'],
    key: str,
    data: PutSessionData,
    response: Response=None
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
        if response:
            response.status_code = 400
        return ErrorResponseModel(error=msg)
    return SuccessResponseModel(data=msg)


@app.put("/session/{session_id}/player/{player_id}/data/{data_type}/{key}/validate")
def put_validate_and_update_player_data(
    session_id: str,
    player_id: str,
    data_type: Literal['int','str'],
    key: str,
    data: PutSessionData,
    response: Response=None
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
        if response:
            response.status_code = 400
        return ErrorResponseModel(error=msg)
    return SuccessResponseModel(data=msg)


@app.get("/session/{session_id}/rule/{data_type}/{key}")
def get_session_data_validation_rules(
    session_id: str,
    data_type: Literal['int','str'],
    key: str,
    response: Response=None
):
    """Get session data validation rules."""
    if data_type == 'int':
        success, msg = api.get_session_data_int_validation_rules(session_id, key)
    elif data_type == 'str':
        success, msg = api.get_session_data_string_validation_rules(session_id, key)
    else:
        success, msg = False, 'Invalid data_type.'
    if success is False:
        if response:
            response.status_code = 400
        return ErrorResponseModel(error=msg)
    return SuccessResponseModel(data=[{
        'val': x[0],
        'operand': x[1]
    } for x in msg])


@app.get("/player/{player_id}")
def get_player(player_id: str, response: Response=None):
    """Get Player address."""
    success, msg = api.get_player(player_id)
    if success is False or not msg:
        if response:
            response.status_code = 400
        return ErrorResponseModel(error=msg)

    return SuccessResponseModel(
        data={
            "player_id": player_id,
            "address": msg.address,
        }
    )
