module.exports = Object.freeze({
  PLAYER_RADIUS: 20,
  PLAYER_MAX_HP: 100,
  PLAYER_SPEED: 400,
  PLAYER_FIRE_COOLDOWN: 0.25,

  BULLET_RADIUS: 3,
  BULLET_SPEED: 800,
  BULLET_DAMAGE: 10,

  SCORE_BULLET_HIT: 20,
  SCORE_PER_SECOND: 1,

  MAP_SIZE: 3000,
  MSG_TYPES: {
    JOIN_GAME: 'join_game',
    GAME_UPDATE: 'update',
    INPUT: 'input',
    BOOST_ON: 'boost_on',
    BOOST_OFF: 'boost_off',
    GAME_OVER: 'dead',
    SHOOT: 'shoot',
    RELEASE_SHOOT: 'release_shoot',
  },

  ANTICHEAT_API_URL: {
    HTTP: 'http://127.0.0.1:8000',
    WS: 'ws://127.0.0.1:8000/ws',
  },
  ANTICHEAT_REQUEST_INTERVAL: 100,
});
