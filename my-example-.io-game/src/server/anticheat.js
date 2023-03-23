const Constants = require('../shared/constants');
const WebSocket = require('ws');

class Anticheat {
  constructor() {
    this.ws = new WebSocket(Constants.ANTICHEAT_API_URL.WS);
    this.makeWsRequest = (action, msg) => JSON.stringify({
      action,
      msg,
    });
  }

  wsAddPlayerToSession(sessionId, playerId) {
    this.ws.send(this.makeWsRequest(
      'post_player_to_session',
      {
        session_id: sessionId,
        player_id: playerId,
      },
    ));
  }

  wsAddPlayerData(sessionId, playerId, dataType, key, data) {
    this.ws.send(this.makeWsRequest(
      'put_validate_and_update_player_data',
      {
        session_id: sessionId,
        player_id: playerId,
        data_type: dataType,
        key,
        data,
      },
    ));
  }

  wsGetPlayerData(sessionId, playerId, dataType, key) {
    this.ws.send(this.makeWsRequest(
      'get_player_data',
      {
        session_id: sessionId,
        player_id: playerId,
        data_type: dataType,
        key,
      },
    ));
  }

  wsAddValidationRule(sessionId, dataType, key, data, operand) {
    this.ws.send(this.makeWsRequest(
      'put_session_data_validation_rule',
      {
        session_id: sessionId,
        data_type: dataType,
        key,
        data,
        operand,
      },
    ));
  }

  wsGetPlayerInSession(sessionId, playerId) {
    this.ws.send(this.makeWsRequest(
      'get_player_in_session',
      {
        session_id: sessionId,
        player_id: playerId,
      },
    ));
  }

  static makeHttpRequest(method, data) {
    return {
      method,
      headers: data && {
        'Content-Type': 'application/json',
      },
      body: data && JSON.stringify(data),
    };
  }

  static async getVersion() {
    console.log('getVersion()');
    const req = await fetch(`${Constants.ANTICHEAT_API_URL.HTTP}/version`);
    return req.json();
  }

  static async addSession() {
    const req = await fetch(
      `${Constants.ANTICHEAT_API_URL.HTTP}/session`,
      Anticheat.makeHttpRequest(
        'POST',
      ),
    );
    return req.json();
  }

  static async getSession(sessionId) {
    const req = await fetch(
      `${Constants.ANTICHEAT_API_URL.HTTP}/session/${sessionId}`,
      Anticheat.makeHttpRequest(
        'GET',
      ),
    );
    return req.json();
  }
  
  static async getPlayer(sessionId, playerId) {
    const req = await fetch(
      `${Constants.ANTICHEAT_API_URL.HTTP}/session/${sessionId}/player/${playerId}`,
      Anticheat.makeHttpRequest(
        'GET',
      ),
    );
    return req.json();
  }

  static async addPlayerToSession(sessionId, playerId) {
    console.log('addPlayerToSession()');
    const req = await fetch(
      `${Constants.ANTICHEAT_API_URL.HTTP}/session/${sessionId}/player/${playerId}`,
      Anticheat.makeHttpRequest(
        'POST',
      ),
    );
    return req.json();
  }

  static async addPlayerData(sessionId, playerId, dataType, key, data) {
    const req = await fetch(
      `${Constants.ANTICHEAT_API_URL.HTTP}/session/${sessionId}/player/${playerId}/data/${dataType}/${key}/validate`,
      Anticheat.makeHttpRequest(
        'PUT',
        {
          data,
        },
      ),
    );
    return req.json();
  }

  static async addValidationRule(sessionId, dataType, key, data, operand) {
    const req = await fetch(
      `${Constants.ANTICHEAT_API_URL.HTTP}/session/${sessionId}/rule/${dataType}/${key}`,
      Anticheat.makeHttpRequest(
        'PUT',
        {
          data,
          operand,
        },
      ),
    );
    return req.json();
  }
}

module.exports = Anticheat;
