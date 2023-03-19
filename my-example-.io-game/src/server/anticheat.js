const Constants = require('../shared/constants');
const WebSocket = require('ws');

class Anticheat {
  constructor() {
    this.ws = new WebSocket(Constants.ANTICHEAT_API_URL.WS);
    this.makeRequestBody = (action, msg) => JSON.stringify({
      action,
      msg,
    });
  }


  wsAddPlayerToSession(sessionId, playerId) {
    this.ws.send(this.makeRequestBody(
      'post_player_to_session',
      {
        session_id: sessionId,
        player_id: playerId,
      },
    ));
  }

  wsAddPlayerData(sessionId, playerId, dataType, key, data) {
    this.ws.send(this.makeRequestBody(
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

  wsAddValidationRule(sessionId, dataType, key, data, operand) {
    this.ws.send(this.makeRequestBody(
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

  static async getVersion() {
    console.log('getVersion()');
    const req = await fetch(`${Constants.ANTICHEAT_API_URL.HTTP}/version`);
    return req.json();
  }

  static async addSession() {
    const req = await fetch(
      `${Constants.ANTICHEAT_API_URL.HTTP}/session`,
      {
        method: 'POST',
      },
    );
    return req.json();
  }

  static async addPlayerToSession(sessionId, playerId) {
    console.log('addPlayerToSession()');
    const req = await fetch(
      `${Constants.ANTICHEAT_API_URL.HTTP}/session/${sessionId}/player/${playerId}`,
      {
        method: 'POST',
      },
    );
    return req.json();
  }

  static async addPlayerData(sessionId, playerId, dataType, key, data) {
    console.log(JSON.stringify({
      data,
    }));
    const req = await fetch(
      `${Constants.ANTICHEAT_API_URL.HTTP}/session/${sessionId}/player/${playerId}/data/${dataType}/${key}/validate`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          data,
        }),
      },
    );
    return req.json();
  }

  static async addValidationRule(sessionId, dataType, key, data, operand) {
    console.log('addValidationRule()');
    const req = await fetch(
      `${Constants.ANTICHEAT_API_URL.HTTP}/session/${sessionId}/rule/${dataType}/${key}`,
      {
        method: 'PUT',
        body: JSON.stringify({
          data,
          operand,
        }),
      },
    );
    return req.json();
  }
}

module.exports = Anticheat;
