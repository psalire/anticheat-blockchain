import json
import sys
import binascii
from web3 import Web3
from web3.exceptions import ContractLogicError

CONTRACT_ADDR = '0xe1325E508C508f8bA2baFf2F85c788B4d4aB984E'

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
if not w3.isConnected():
    print('isConnected() false. Exiting...')
    sys.exit(0)

with open('build/contracts/Anticheat.json') as fd:
    abi = json.load(fd)['abi']

contract_obj = w3.eth.contract(address=CONTRACT_ADDR, abi=abi)
try:
    print(binascii.hexlify(
        contract_obj.functions
        .add_new_player('helloworld')
        .transact({'from': w3.eth.accounts[0]})
    ))
except ContractLogicError:
    print('Success, caught expected exception')

try:
    print(binascii.hexlify(
        contract_obj.functions
        .add_new_player('helloworld3')
        .transact({'from': w3.eth.accounts[0]})
    ))
except ContractLogicError:
    print('Success, caught expected exception')
print('')

print(contract_obj.functions.players('helloworld').call())
print(contract_obj.functions.players('helloworld2').call())
print(contract_obj.functions.players('helloworld3').call())
