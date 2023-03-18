"""Communication to Ethereum blockchain with w3."""
import sys
import json
from web3 import Web3
from web3.exceptions import ContractLogicError

CONTRACT_ADDR = '0x3440B06F0C6dE258C8ff79AEab2Db248F28ED368'


class W3Facade:
    """Smart contract functions."""

    def __init__(self, url='http://127.0.0.1:7545'):
        """Initialize Web3 interface to contract."""
        self.w3 = Web3(Web3.HTTPProvider(url))
        if not self.w3.isConnected():
            print('w3.isConnected() false. Exiting...')
            sys.exit(0)
        with open('Anticheat.json', encoding='utf-8') as file:
            self.anticheat_abi = json.load(file)['abi']
        with open('SessionHandler.json', encoding='utf-8') as file:
            self.session_handler_abi = json.load(file)['abi']
        with open('Session.json', encoding='utf-8') as file:
            self.session_abi = json.load(file)['abi']
        with open('Player.json', encoding='utf-8') as file:
            self.player_abi = json.load(file)['abi']
        self.anticheat = self.w3.eth.contract(address=CONTRACT_ADDR, abi=self.anticheat_abi)
        self.session_handler = self.w3.eth.contract(
            address=self.anticheat.functions.session_handler().call(),
            abi=self.session_handler_abi
        )
        self.account = self.w3.eth.accounts[0]

    def contract_function(fun):
        def wrapper(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            except ContractLogicError as err:
                return False, str(err)
        return wrapper

    @contract_function
    def add_session(self, session_id):
        """Create new session."""
        (self.session_handler.functions
            .add_new_session(session_id)
            .transact({'from': self.account}))
        return True, None

    @contract_function
    def add_player_to_session(self, session_id, player_id):
        """Add player to existing session."""
        (self.session_handler.functions
            .add_new_player(session_id, player_id)
            .transact({'from': self.account}))
        return True, None

    @contract_function
    def get_int_session_data(self, session_id, key):
        """Get int session data."""
        success, session = self.get_session(session_id, handle_exception=False)
        if success is False:
            return False, "Failed to retrieve session."
        return True, session.functions.get_int_data(key).call()

    @contract_function
    def get_string_session_data(self, session_id, key):
        """Get int session data."""
        success, session = self.get_session(session_id, handle_exception=False)
        if success is False:
            return False, "Failed to retrieve session."
        return True, session.functions.get_string_data(key).call()

    @contract_function
    def put_int_session_data(self, session_id, key, data):
        """Put int session data."""
        success, session = self.get_session(session_id, handle_exception=False)
        if success is False:
            return False, "Failed to retrieve session."
        session.functions.update_int_data(
            key, data
        ).transact({
            'from': self.account
        })
        return True, None

    @contract_function
    def put_string_session_data(self, session_id, key, data):
        """Put int session data."""
        success, session = self.get_session(session_id, handle_exception=False)
        if success is False:
            return False, "Failed to retrieve session."
        session.functions.update_string_data(
            key, data
        ).transact({
            'from': self.account
        })
        return True, None

    @contract_function
    def put_int_session_data_validation_rule(self, session_id, key, val, operand):
        """Put session int validation data rule."""
        success, session = self.get_session(session_id, handle_exception=False)
        if success is False:
            return False, "Failed to retrieve session."
        session.functions.add_int_validation_rule(
            key, val, operand
        ).transact({
            'from': self.account
        })
        return True, None

    @contract_function
    def put_string_session_data_validation_rule(self, session_id, key, val, operand):
        """Put session string validation data rule."""
        success, session = self.get_session(session_id, handle_exception=False)
        if success is False:
            return False, "Failed to retrieve session."
        session.functions.add_string_validation_rule(
            key, val, operand
        ).transact({
            'from': self.account
        })
        return True, None

    @contract_function
    def get_session_data_int_validation_rules(self, session_id, key):
        """Get session int validation rules."""
        success, session = self.get_session(session_id, handle_exception=False)
        if success is False:
            return False, "Failed to retrieve session."
        return True, session.functions.get_int_validation_rules(key).call()

    @contract_function
    def get_session_data_string_validation_rules(self, session_id, key):
        """Get session string validation rules."""
        success, session = self.get_session(session_id, handle_exception=False)
        if success is False:
            return False, "Failed to retrieve session."
        return True, session.functions.get_string_validation_rules(key).call()

    @contract_function
    def put_validate_and_update_session_int_data(self, session_id, key, data):
        """Put session int data while validating."""
        self.anticheat.functions.validate_and_update_session_int_data(
            session_id, key, data
        ).transact({'from': self.account})
        return True, None

    @contract_function
    def put_validate_and_update_session_string_data(self, session_id, key, data):
        """Put session string data while validating."""
        self.anticheat.functions.validate_and_update_session_string_data(
            session_id, key, data
        ).transact({'from': self.account})
        return True, None

    def get_session(self, session_id, handle_exception=True):
        """Get Session contract."""
        try:
            session_addr = (self.session_handler.functions
                            .get_session(session_id)
                            .call())
            return True, self.w3.eth.contract(
                address=session_addr,
                abi=self.session_abi
            )
        except ContractLogicError as err:
            if not handle_exception:
                raise ContractLogicError(err) from err
            return False, str(err)

    @contract_function
    def get_player(self, player_id):
        """Get Player contract."""
        player_addr = (self.session_handler.functions
                    #    .session_handler()
                       .get_player(player_id)
                       .call())
        return True, self.w3.eth.contract(
            address=player_addr,
            abi=self.player_abi
        )

    @contract_function
    def get_player_in_session(self, session_id, player_id):
        """Get Player contract."""
        player_addr = (self.session_handler.functions
                            .get_player_in_session(session_id, player_id)
                            .call())
        return True, self.w3.eth.contract(
            address=player_addr,
            abi=self.player_abi
        )

    @contract_function
    def get_player_position(self, session_id, player_id):
        """Get Player position."""
        success, player = self.get_player_in_session(session_id, player_id)
        # success, player = self.get_player(player_id)
        if success is False:
            return False, str("Failed to retrieve player.")
        return True, player.functions.get_position().call()
