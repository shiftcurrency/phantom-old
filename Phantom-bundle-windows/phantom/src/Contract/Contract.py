import json
from Phantom import Phantom_Ui
from tools import utils
from tools.abi import encode_abi, decode_abi


class ContractCall(object):

    def _encode_function(self, signature, param_values):

        prefix = utils.big_endian_to_int(utils.sha3(signature)[:4])
        
        if signature.find('(') == -1:
            raise RuntimeError('Invalid function signature. Missing "(" and/or ")"...')

        if signature.find(')') - signature.find('(') == 1:
            return utils.encode_int(prefix)

        types = signature[signature.find('(') + 1: signature.find(')')].split(',')
        print "types: %s" % types
        print "params values: %s" %param_values
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
        self.phantom_ui = Phantom_Ui.Phantom_Ui()
        postparams = {"params" : [{"to" : address, "data" : data_hex}]}
        call_res = self.phantom_ui.call(postparams)
        if 'result' in call_res and len(call_res['result']) > 2:
            return decode_abi(result_types, call_res['result'][2:].decode('hex'))

    def call_with_transaction(self, pd):
        
        data = self._encode_function(pd['function_signature'],pd['function_argument'])
        data_hex = data.encode('hex')
        postparams = { 'params' : [{ 'from' : pd['from'], 'to' : pd['to'], 'gas' : pd['gas'], 'data' : data_hex, 'password' : pd['password'], 'method' : 'call_contract' }]}
        self.phantom_ui = Phantom_Ui.Phantom_Ui()
        res = self.phantom_ui.send_transaction(postparams)
        return res
