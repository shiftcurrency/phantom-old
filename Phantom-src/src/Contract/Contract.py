import json
from Phantom import Phantom_Ui
from tools import utils
from tools.abi import encode_abi, decode_abi


class ContractCall(object):

    BLOCK_TAG_LATEST="latest"

    def _encode_function(self, signature, param_values):

        prefix = utils.big_endian_to_int(utils.sha3(signature)[:4])

        if signature.find('(') == -1:
            raise RuntimeError('Invalid function signature. Missing "(" and/or ")"...')

        if signature.find(')') - signature.find('(') == 1:
            return utils.encode_int(prefix)

        types = signature[signature.find('(') + 1: signature.find(')')].split(',')
        encoded_params = encode_abi(types, param_values)
        return utils.zpad(utils.encode_int(prefix), 4) + encoded_params

    def create_contract(self, from_, code, gas, passwd, sig=None, args=None):
        
        if sig is not None and args is not None:
             types = sig[sig.find('(') + 1: sig.find(')')].split(',')
             encoded_params = encode_abi(types, args)
             code += encoded_params.encode('hex')

        self.phantom_ui = Phantom_Ui.Phantom_Ui()
        """ Tag the transaction with create_contract. Create contract does not have a reciever """
        postparams = { 'params' : [{ 'from' : from_, 'gas' : gas, 'data' : code, 'password' : passwd, 'method' : 'create_contract' }]}
        try:
            contract_tx = self.phantom_ui.send_transaction(postparams)
            if 'result' in contract_tx:
                return contract_tx['result']
        except Exception as e:
            return "False"
        return "False"

    def call(self, address, sig, args, result_types):
        
        data = self._encode_function(sig, args)
        data_hex = data.encode('hex')
        response = self.shf_call(to_address=address, data=data_hex)
        return decode_abi(result_types, response[2:].decode('hex'))

    def call_with_transaction(self, pd):
        
        data = self._encode_function(pd['function_signature'],pd['function_argument'])
        data_hex = data.encode('hex')
        postparams = { 'params' : [{ 'from' : pd['from'], 'to' : pd['to'], 'gas' : pd['gas'], 'data' : data_hex, 'password' : pd['password'], 'method' : 'call_contract' }]}
        self.phantom_ui = Phantom_Ui.Phantom_Ui()
        res = self.phantom_ui.send_transaction(postparams)
        return res

    def shf_getStorageAt(self, address=None, position=0, block=BLOCK_TAG_LATEST):
        '''
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shf_getstorageat

        TESTED
        '''
        block = validate_block(block)
        return self._call('shf_getStorageAt', [address, hex(position), block])

    def shf_getCode(self, address, default_block=BLOCK_TAG_LATEST):
        '''
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shf_getcode

        NEEDS TESTING
        '''
        if isinstance(default_block, basestring):
            if default_block not in BLOCK_TAGS:
                raise ValueError
        return self._call('shf_getCode', [address, default_block])

    def shf_sendTransaction(self, to_address=None, from_address=None, gas=None, gas_price=None, value=None, data=None,
                            nonce=None):
        '''
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shf_sendtransaction

        NEEDS TESTING
        '''
        params = {}
        params['from'] = from_address or self.shf_shiftbase()
        if to_address is not None:
            params['to'] = to_address
        if gas is not None:
            params['gas'] = hex(gas)
        if gas_price is not None:
            params['gasPrice'] = hex(gas_price)
        if value is not None:
            params['value'] = hex(value)
        if data is not None:
            params['data'] = data
        if nonce is not None:
            params['nonce'] = hex(nonce)
        return self._call('shf_sendTransaction', [params])

    def shf_sendRawTransaction(self, data):
        '''
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shf_sendrawtransaction

        NEEDS TESTING
        '''
        return self._call('shf_sendRawTransaction', [data])

    def shf_call(self, to_address, from_address=None, gas=None, gas_price=None, value=None, data=None,
                 default_block=BLOCK_TAG_LATEST):
        '''
        https://github.com/ethereum/wiki/wiki/JSON-RPC#shf_call

        NEEDS TESTING
        '''
        if isinstance(default_block, basestring):
            if default_block not in BLOCK_TAGS:
                raise ValueError
        obj = {}
        obj['to'] = to_address
        if from_address is not None:
            obj['from'] = from_address
        if gas is not None:
            obj['gas'] = hex(gas)
        if gas_price is not None:
            obj['gasPrice'] = hex(gas_price)
        if value is not None:
            obj['value'] = value
        if data is not None:
            obj['data'] = data
        return self._call('shf_call', [obj, default_block])
