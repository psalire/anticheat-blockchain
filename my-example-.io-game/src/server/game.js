const Constants = require('../shared/constants');
const Player = require('./player');
const Anticheat = require('./anticheat');
const applyCollisions = require('./collisions');

class Game {
  constructor(anticheat) {
    this.anticheat = anticheat;
    this.anticheat.ws.addEventListener('message', event => {
      const msg = JSON.parse(event.data);
      console.log('Received message:', msg);
      if (Object.hasOwn(msg.response, 'error') &&
          msg.response.error.includes('Player flagged')) {
        this.removePlayerById(msg.response.data.player_id);
      } else if (msg.action === 'get_player_data') {
        if (msg.response.val < 0) {
          this.removePlayerById(msg.response.player_id);
        } else {
          this.anticheat.wsAddPlayerData(
            this.sessionId,
            msg.response.player_id,
            'int',
            'ammo',
            [msg.response.val - 1],
          );
        }
      }
    });
    this.sessionReady = false;
    Anticheat.addSession().then(async data => {
      this.sessionId = data.data.session_id;
      do {
        console.log('waiting for session...');
        // eslint-disable-next-line no-await-in-loop
        await new Promise(r => setTimeout(r, 3000)); // sleep 1000
        // eslint-disable-next-line no-await-in-loop
        let status = (await Anticheat.getSession(this.sessionId)).status;
        this.sessionReady = status === 'success';
      } while (!this.sessionReady);
      Anticheat.addValidationRule(
        this.sessionId,
        'int',
        'x',
        Math.round((Constants.MAP_SIZE - 100) * 100),
        'gt',
      ).then(ret => console.log(ret));
      Anticheat.addValidationRule(
        this.sessionId,
        'int',
        'y',
        Math.round((Constants.MAP_SIZE - 100) * 100),
        'gt',
      );
      Anticheat.addValidationRule(
        this.sessionId,
        'int',
        'x',
        100,
        'lt',
      );
      Anticheat.addValidationRule(
        this.sessionId,
        'int',
        'y',
        100,
        'lt',
      );
      Anticheat.addValidationRule(
        this.sessionId,
        'int',
        'ammo',
        0,
        'lt',
      );
      Anticheat.addValidationRule(
        this.sessionId,
        'int',
        'speedboosts',
        0,
        'lt',
      );
    });
    this.sockets = {};
    this.players = {};
    this.bullets = [];
    this.lastUpdateTime = Date.now();
    this.shouldSendUpdate = false;
    setInterval(this.update.bind(this), 1000 / 60);
  }

  async addPlayer(socket, username) {
    while (!this.sessionReady) {
      // eslint-disable-next-line no-await-in-loop
      console.log('addPlayer() wait for session...')
      await new Promise(r => setTimeout(r, 1000)); // sleep 1000
    }
    this.anticheat.wsAddPlayerToSession(this.sessionId, socket.id);
    this.sockets[socket.id] = socket;

    // Generate a position to start this player at.
    const x = Constants.MAP_SIZE * (0.25 + Math.random() * 0.5);
    const y = Constants.MAP_SIZE * (0.25 + Math.random() * 0.5);
    this.players[socket.id] = new Player(socket.id, username, x, y, this.sessionId, this.anticheat);
    let playerReady = false;
    do {
      console.log('waiting for player...');
      // eslint-disable-next-line no-await-in-loop
      await new Promise(r => setTimeout(r, 3000)); // sleep 1000
      // eslint-disable-next-line no-await-in-loop
      let status = (await Anticheat.getPlayer(this.sessionId, socket.id)).status;
      playerReady = status === 'success';
    } while (!playerReady);
    this.players[socket.id].setPlayerReady(true);
  }

  removePlayer(socket) {
    delete this.sockets[socket.id];
    delete this.players[socket.id];
  }

  removePlayerById(playerId) {
    const socket = this.sockets[playerId];
    if (socket) {
      console.log(`Remove: ${socket.id}`);
      this.removePlayer(socket);
    }
  }

  handleInput(socket, dir) {
    if (this.players[socket.id]) {
      this.players[socket.id].setDirection(dir);
    }
  }

  turnOnBoost(socket) {
    if (this.players[socket.id]) {
      this.players[socket.id].turnOnBoost();
    }
  }

  turnOffBoost(socket) {
    if (this.players[socket.id]) {
      this.players[socket.id].turnOffBoost();
    }
  }

  shoot(socket) {
    if (this.players[socket.id]) {
      this.players[socket.id].turnOnShoot();
    }
  }

  releaseShoot(socket) {
    if (this.players[socket.id]) {
      this.players[socket.id].releaseShoot();
    }
  }

  update() {
    // Calculate time elapsed
    const now = Date.now();
    const dt = (now - this.lastUpdateTime) / 1000;
    this.lastUpdateTime = now;

    // Update each bullet
    const bulletsToRemove = [];
    this.bullets.forEach(bullet => {
      if (bullet.update(dt)) {
        // Destroy this bullet
        bulletsToRemove.push(bullet);
      }
    });
    this.bullets = this.bullets.filter(bullet => !bulletsToRemove.includes(bullet));

    // Update each player
    Object.keys(this.sockets).forEach(playerID => {
      const player = this.players[playerID];
      const newBullet = player.update(dt);
      if (newBullet) {
        this.bullets.push(newBullet);
      }
    });

    // Apply collisions, give players score for hitting bullets
    const destroyedBullets = applyCollisions(Object.values(this.players), this.bullets);
    destroyedBullets.forEach(b => {
      if (this.players[b.parentID]) {
        this.players[b.parentID].onDealtDamage();
      }
    });
    this.bullets = this.bullets.filter(bullet => !destroyedBullets.includes(bullet));

    // Check if any players are dead
    Object.keys(this.sockets).forEach(playerID => {
      const socket = this.sockets[playerID];
      const player = this.players[playerID];
      if (player.hp <= 0) {
        socket.emit(Constants.MSG_TYPES.GAME_OVER);
        this.removePlayer(socket);
      }
    });

    // Send a game update to each player every other time
    if (this.shouldSendUpdate) {
      const leaderboard = this.getLeaderboard();
      Object.keys(this.sockets).forEach(playerID => {
        const socket = this.sockets[playerID];
        const player = this.players[playerID];
        socket.emit(Constants.MSG_TYPES.GAME_UPDATE, this.createUpdate(player, leaderboard));
      });
      this.shouldSendUpdate = false;
    } else {
      this.shouldSendUpdate = true;
    }
  }

  getLeaderboard() {
    return Object.values(this.players)
      .sort((p1, p2) => p2.score - p1.score)
      .slice(0, 5)
      .map(p => ({ username: p.username, score: Math.round(p.score) }));
  }

  createUpdate(player, leaderboard) {
    const nearbyPlayers = Object.values(this.players).filter(
      p => p !== player && p.distanceTo(player) <= Constants.MAP_SIZE / 2,
    );
    const nearbyBullets = this.bullets.filter(
      b => b.distanceTo(player) <= Constants.MAP_SIZE / 2,
    );

    return {
      t: Date.now(),
      me: player.serializeForUpdate(),
      others: nearbyPlayers.map(p => p.serializeForUpdate()),
      bullets: nearbyBullets.map(b => b.serializeForUpdate()),
      leaderboard,
    };
  }
}

module.exports = Game;
