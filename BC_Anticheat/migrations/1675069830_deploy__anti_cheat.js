const AntiCheatContract = artifacts.require("AntiCheat");
// const PlayerContract = artifacts.require("Player");
const SessionContract = artifacts.require("Session");
// const OperandsLib = artifacts.require("OperandsLib");
const ValidationRulesLib = artifacts.require("ValidationRulesLib");
const ValidationLib = artifacts.require("ValidationLib");

module.exports = function(_deployer) {
    // Use deployer to state migration tasks.
    // _deployer.deploy(OperandsLib);
    _deployer.deploy(ValidationRulesLib);
    _deployer.deploy(ValidationLib);
    // _deployer.link(OperandsLib, SessionContract);
    _deployer.link(ValidationRulesLib, ValidationLib);
    _deployer.link(ValidationRulesLib, SessionContract);
    _deployer.link(ValidationLib, SessionContract);
    _deployer.link(ValidationLib, AntiCheatContract);
    // _deployer.link(OperandsLib, AntiCheatContract);
    // _deployer.link(ValidationRulesLib, AntiCheatContract);
    // _deployer.link(AntiCheatContract, ValidationRulesLib);
    _deployer.deploy(AntiCheatContract);
    // _deployer.deploy(PlayerContract, "DUMMYPLAYER");
    // _deployer.deploy(SessionContract, "DUMMYSESSION");
};
