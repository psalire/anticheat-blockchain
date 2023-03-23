const ObjectClass = require('./object');
const Bullet = require('./bullet');
const Constants = require('../shared/constants');

class Player extends ObjectClass {
  constructor(id, username, x, y, sessionId, anticheat) {
    super(id, x, y, Math.random() * 2 * Math.PI, Constants.PLAYER_SPEED);
    this.anticheat = anticheat;
    this.anticheatInterval = 0;
    this.username = username;
    this.hp = Constants.PLAYER_MAX_HP;
    this.fireCooldown = 0;
    this.score = 0;
    this.shoot = false;
    this.shot = false;
    this.sessionId = sessionId;
    this.playerReady = false;
  }

  // Returns a newly created bullet, or null.
  update(dt) {
    if (!this.playerReady) {
      return;
    }
    super.update(dt);

    // Update score
    this.score += dt * Constants.SCORE_PER_SECOND;

    // Make sure the player stays in bounds
    this.x = Math.max(0, Math.min(Constants.MAP_SIZE, this.x));
    this.y = Math.max(0, Math.min(Constants.MAP_SIZE, this.y));
    if (this.anticheatInterval === 0) {
      console.log('send player data');
      this.anticheat.wsAddPlayerData(this.sessionId, this.id, 'int', 'x', [Math.round(this.x * 100)]);
      this.anticheat.wsAddPlayerData(this.sessionId, this.id, 'int', 'y', [Math.round(this.y * 100)]);
      this.anticheat.wsAddPlayerData(this.sessionId, this.id, 'int', 'ammo', [30]);
      this.anticheat.wsAddPlayerData(this.sessionId, this.id, 'int', 'speedboosts', [3]);
      this.anticheatInterval = Constants.ANTICHEAT_REQUEST_INTERVAL;
    } else {
      this.anticheatInterval--;
    }
    
    // Fire a bullet, if needed
    this.fireCooldown -= dt;
    if (this.shoot && !this.shot && this.fireCooldown <= 0) {
      // this.anticheat.wsAddPlayerData(this.sessionId, this.id, 'int', 'x', [Math.round(this.x * 100)]);
      // this.anticheat.wsAddPlayerData(this.sessionId, this.id, 'int', 'y', [Math.round(this.y * 100)]);
      this.fireCooldown += Constants.PLAYER_FIRE_COOLDOWN;
      this.shot = true;
      return new Bullet(this.id, this.x, this.y, this.direction);
    }

    return null;
  }

  setPlayerReady(val) {
    this.playerReady = val;
  }

  takeBulletDamage() {
    this.hp -= Constants.BULLET_DAMAGE;
  }

  onDealtDamage() {
    this.score += Constants.SCORE_BULLET_HIT;
  }

  turnOnBoost() {
    super.setSpeed(Constants.PLAYER_SPEED * 3);
  }

  turnOffBoost() {
    super.setSpeed(Constants.PLAYER_SPEED);
  }

  turnOnShoot() {
    this.shoot = true;
  }

  releaseShoot() {
    this.shoot = false;
    this.shot = false;
  }

  serializeForUpdate() {
    return {
      ...(super.serializeForUpdate()),
      direction: this.direction,
      hp: this.hp,
    };
  }
}

module.exports = Player;
