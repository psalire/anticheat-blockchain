// Learn more about this file at:
// https://victorzhou.com/blog/build-an-io-game-part-1/#6-client-input-%EF%B8%8F
import {
  updateDirection,
  turnOnBoost,
  turnOffBoost,
  shoot,
  releaseShoot,
} from './networking';

let SPACE_DOWN = false;
let SHIFT_DOWN = false;
let BULLETS = 30;
let BOOSTS = 3;
let BOOST_ON = false;
const ammoDiv = document.getElementById('ammo');
const boostsDiv = document.getElementById('boosts');

function onMouseInput(e) {
  handleInput(e.clientX, e.clientY);
}

function onTouchInput(e) {
  const touch = e.touches[0];
  handleInput(touch.clientX, touch.clientY);
}

function onKeydown(e) {
  switch (e.code) {
    case 'ShiftLeft':
    case 'ShiftRight':
      handleTurnOnBoost();
      break;
    case 'Space':
      handleShoot();
      break;
    default:
  }
}

function onKeyup(e) {
  switch (e.code) {
    case 'ShiftLeft':
    case 'ShiftRight':
      SHIFT_DOWN = false;
      break;
    case 'Space':
      handleReleaseShoot();
      break;
    default:
  }
}

function handleInput(x, y) {
  const dir = Math.atan2(x - window.innerWidth / 2, window.innerHeight / 2 - y);
  updateDirection(dir);
}

function handleTurnOnBoost() {
  if (!SHIFT_DOWN && !BOOST_ON && BOOSTS > 0) {
    console.log('Boost!');
    turnOnBoost();
    setTimeout(handleTurnOffBoost, 3000);
    SHIFT_DOWN = true;
    BOOST_ON = true;
    BOOSTS--;
    boostsDiv.innerText = BOOSTS;
  }
}

function handleTurnOffBoost() {
  console.log('Boost off!');
  turnOffBoost();
  BOOST_ON = false;
}

function handleShoot() {
  if (!SPACE_DOWN && BULLETS > 0) {
    console.log('Shoot!');
    shoot();
    SPACE_DOWN = true;
    BULLETS--;
    console.log(BULLETS);
    ammoDiv.innerText = BULLETS;
  }
}

function handleReleaseShoot() {
  if (SPACE_DOWN) {
    console.log('Release shoot!');
    releaseShoot();
    SPACE_DOWN = false;
  }
}

export function startCapturingInput() {
  window.addEventListener('mousemove', onMouseInput);
  window.addEventListener('click', onMouseInput);
  window.addEventListener('touchstart', onTouchInput);
  window.addEventListener('touchmove', onTouchInput);

  window.addEventListener('keydown', onKeydown);
  window.addEventListener('keyup', onKeyup);
}

export function stopCapturingInput() {
  window.removeEventListener('mousemove', onMouseInput);
  window.removeEventListener('click', onMouseInput);
  window.removeEventListener('touchstart', onTouchInput);
  window.removeEventListener('touchmove', onTouchInput);

  window.removeEventListener('keydown', onKeydown);
}
