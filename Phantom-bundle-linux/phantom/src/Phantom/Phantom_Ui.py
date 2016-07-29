""" Copyright (C) Shift Cryptocurrency - Joey, <shiftcurrency@gmail.com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA. """

import json
import Error_Msg
import Run_Method
from Shift_IPC import IPC_Client
import Phantom_Db
import logging
import main

class Phantom_Ui(object):

    def __init__(self):
        self.error_msg = Error_Msg.Error_Msg()
        self.run_method = Run_Method.Run_Method()

    def create_phantom_site(self):

        from Config import config
        from Crypt import CryptBitcoin
        from Site import Site
        import os

        config.parse(silent=True)
        if not config.arguments:
            config.parse()

        self.private_key = CryptBitcoin.newPrivatekey()
        self.address = CryptBitcoin.privatekeyToAddress(self.private_key)

        try:
            os.mkdir("%s/%s" % (config.data_dir, self.address))
            open("%s/%s/index.html" % (config.data_dir, self.address), "w").write("Hello %s!" % self.address)
        except Exception as e:
            return self.error_msg.error_response("err_create_sitedir")
    
        try:
            self.site = Site(self.address)
            self.site.content_manager.sign(privatekey=self.private_key, extend={"postmessage_nonce_security": True})
            self.site.settings["own"] = True
            self.site.saveSettings()
        except Exception as e:
            print e
            return self.error_msg.error_response("err_create_site")
        return {"jsonrpc": "2.0", "id": "1", "result": ["true", str(self.address), str(self.private_key)]}


    def validate_postdata(self,postdata):


        try:
            """ 
            Convert the HTTP body json string into a dictionary. A non valid json string will return false.
            """
            postparams = json.loads(postdata)
        except Exception as e:
            print e
            return self.error_msg.error_response("invalid_json_req")

        if 'jsonrpc' in postparams and not postparams['jsonrpc'] == '2.0':
            return self.error_msg.error_response("invalid_json_ver")

        if 'method' in postparams and len(postparams['method']) == 0:
            return self.error_msg.error_response("no_method")

        if not 'params' in postparams:
            print "here"
            return self.error_msg.error_response("missing_params")

        return postparams


    def run_method(self,postparams):

        self.res = self.run_method.execute(postparams)
        return self.res


    def get_shiftbase(self,postparams):

        if len(postparams['params']) == 0:
            try:
                self.client = IPC_Client.Client()
                self.res = self.client.get_shiftbase()
                return self.res
            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("no_params_allowed")


    def get_peercount(self,postparams):
    
        if len(postparams['params']) == 0:
            try:
                self.client = IPC_Client.Client()
                self.res = self.client.get_peercount()
                if 'result' in self.res:
                    self.res['result'] = str(int(self.res['result'], 16))
                return self.res

            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("no_params_allowed")



    def get_blocknumber(self,postparams):

        if len(postparams['params']) == 0:
            try:
                self.client = IPC_Client.Client()
                self.res = self.client.get_blocknumber()
                if 'result' in self.res:
                    self.res['result'] = str(int(self.res['result'], 16))
                return self.res

            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("no_params_allowed")


    def get_block_data(self,postparams):

        if len(postparams['params']) == 2:
            if postparams['params'][1] == "true" or postparams['params'][1] == "false":
                try:
                    self.client = IPC_Client.Client()
                    self.res = self.client.get_block_data(postparams['params'][0], postparams['params'][1])
                    return self.res
                except Exception as e:
                    return self.error_msg.error_response("ipc_call_error")
            return self.error_msg.error_response("invalid_parameters")
        return self.error_msg.error_response("missing_params")


    def rr_ptr(self,postparams):

        if len(postparams['params']) == 1:
            if not postparams['params'][0][:-6].isalnum() and not postparams[param].endswith('.shift'):
                return self.error_msg.error_response("invalid_domain")
            else:
                pass

        return self.error_msg.error_response("")


    def get_accounts(self,postparams):

        if len(postparams['params']) == 0:
            try:
                self.client = IPC_Client.Client()
                self.res = self.client.get_accounts()
                return self.res
            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("no_params_allowed")


    def get_balance(self,postparams):

        if len(postparams['params']) == 2:
            self.addr = postparams['params'][0]
            self.when = postparams['params'][1]

            if not self.verify_wallet_addr(self.addr):
                return self.error_msg.error_response("invalid_wallet_addr")

            if self.when == "latest" or self.when == "pending" or self.when == "earliest":

                try:
                    self.client = IPC_Client.Client()
                    self.res = self.client.get_balance(self.addr, self.when)
                    if 'result' in self.res:
                        self.res['result'] = str(int(self.res['result'], 16))
                    return self.res
                except Exception as e:
                    return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("missing_params")
            
 

    def sign_publish_site(self,postparams):

        from Site import Site

        if not len(postparams['params']) == 2 and not len(postparams['params'][0]) == 34:
            return self.error_msg.error_response("sign_missing_params")


        address = postparams['params'][0]
        privatekey = postparams['params'][1]
        site = Site(address, allow_create=False)

        try:
            inner_path="content.json"
            success = site.content_manager.sign(inner_path, privatekey=privatekey, update_changed_files=True)
            if success:
                publisher = main.Actions()
                publisher.sitePublish(address, inner_path=inner_path)
        except Exception as e:
            print e
            return self.error_msg.error_response("err_sign_site")
        

        return {"jsonrpc": "2.0", "id": "1", "result": ["true", str(address)]}



    def unlock_account(self, addr, password):

        if not self.verify_wallet_addr(addr):
            return self.error_msg.error_response("invalid_wallet_addr")

        elif not len(password) > 0:
            return self.error_msg.error_response("empty_password")

        else:
            try:
                self.client = IPC_Client.Client()
                self.res = self.client.unlock_account(addr, password)
                return self.res
            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")


    def lock_account(self, addr):

        if not self.verify_wallet_addr(addr):
            return self.error_msg.error_response("invalid_wallet_addr")

        try:
            self.client = IPC_Client.Client()
            self.res = self.client.lock_account(addr)
            return self.res
        except Exception as e:
            return self.error_msg.error_response("ipc_call_error")


    def create_site(self,postparams):

        if len(postparams['params']) == 0:
            return self.create_phantom_site()

        return self.error_msg.error_response("")


    def create_account(self,postparams):

        if len(postparams['params']) == 1:
            if len(postparams['params'][0]) == 0:
                return self.error_msg.error_response("empty_password")
            try:
                self.client = IPC_Client.Client()
                self.res = self.client.create_account(postparams['params'][0])
                return self.res
            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")


    def net_listening(self,postparams):

        if len(postparams['params']) == 0:
            try:
                self.client = IPC_Client.Client()
                self.res = client.net_listening()
                return self.res
            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("no_params_allowed")


    def verify_wallet_addr(self, addr):
        
        try:
            int(addr, 16) 
        except ValueError as e:
            return False

        if not len(addr) >= 40: 
            return False
        
        return True
 

    def send_transaction(self,postparams):

        if len(postparams['params']) == 1:
            self.pd = postparams['params'][0]
            
            if not self.verify_wallet_addr(postparams['params'][0]['from']):
                return self.error_msg.error_response("invalid_wallet_addr")

            if not 'to' in self.pd:
                self.pd['to'] = False

            if 'amount' in self.pd:
                try:
                    self.pd['amount'] = int(float(self.pd['amount'])*1000000000000000000)
                    self.pd['amount'] = "0x" + format(self.pd['amount'], 'x')
                except Exception as e:
                    print e
                    return self.error_msg.error_response("invalid_amount")

            if 'data' in self.pd and len(self.pd['data']) == 0:
                self.pd['data'] = False

            if 'gas' in self.pd and len(self.pd['gas']) == 0:
                """ Default gas amount for a transaction """
                self.pd['gas'] = '30000'

            if 'password' in self.pd and len(self.pd['password']) == 0:
                return self.error_msg.error_response("empty_password")

            """ TODO: check unlock success """
            self.res = self.unlock_account(self.pd['from'], self.pd['password'])

            """ Tag the transaction with either create_contract or send_transaction.
                create_contract does not have a reciever """
            if 'method' not in self.pd:
                self.pd['method'] = 'send_transaction'

            self.client = IPC_Client.Client()

            try:
                self.res = self.client.send_transaction(self.pd)
            except Exception as e:
                print e
                return self.error_msg.error_response("ipc_call_error")

            return self.res

    def send_rawtransaction(self,postparams):

        if len(postparams['params']) == 1:
            try:
                int(postparams['params'][0], 16)
            except Exception as e:
                return self.error_msg.error_response("invalid_hex_string")
        
            try:
                self.res = self.client.send_transaction(postparams['params'][0])
                return res
            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("invalid_parameters")


    def create_shh_filter(self,postparams):
    
        if len(postparams['params']) == 1:
            self.pd = postparams['params'][0]
            if 'to' in self.pd and 'topics' in self.pd:

                if not self.verify_wallet_addr(self.pd['to']):
                    return self.error_msg.error_response("invalid_wallet_addr")

                if self.pd['topics'] == "":
                    return self.error_msg.error_response("err_create_filter")
                params = {"to": str(self.pd['to']), "topics": [str(self.pd['topics'][0].encode("hex"))]}
                self.client = IPC_Client.Client()
                try:
                    self.res = self.client.create_shh_filter(params)
                    return self.res
                except Exception as e:
                    return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("missing_params")


    def new_message_ident(self,postparams):

        if len(postparams['params']) == 0:
            self.client = IPC_Client.Client()
            try:
                self.res = client.new_message_ident()
                return self.res
            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("no_params_allowed")


    def message_ident_exists(self,postparams):
        if len(postparams['params']) == 1:
            try:
                int(postparams['params'][0], 16)
            except:
                return self.error_msg.error_response("invalid_hex_string")

            self.client = IPC_Client.Client()
            try:
                self.res = self.client.message_ident_exists(postparams['params'][0])
                return self.res 
            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("missing_params")


    def send_message(self,postparams):

        if len(postparams['params']) == 1:
            self.pd = postparams['params'][0]

            if 'to' in self.pd and 'message' in self.pd and self.pd['message'] != "":

                if not self.verify_wallet_addr(self.pd['to']):
                    return self.error_msg.error_response("invalid_wallet_addr")


                self.from_ident = self.new_message_ident({'params':''})
                if 'result' in self.from_ident and len(self.from_ident['result']) == 2:
                    return self.error_msg.error_response("err_gen_ident")

                self.pd['from'] = self.from_ident['result']
                self.pd['topics'] = ['{"type":"c","store-encrypted":"true"}'.encode("hex")]
                self.pd['priority'] = "0x64"
                self.pd['ttl'] = "0x64"
                self.pd['message'] = self.pd['message'].encode("hex")

                """ Create filter to wait for incoming answers. Use postparams with the unhexed strings. """
                self.res  = self.create_shh_filter(postparams)

                try:
                    int(self.res['result'], 16)
                except:
                    return self.error_msg.error_response("err_create_filter")

                self.phantomdb = Phantom_Db.PhantomDb()
                self.store = {'to':self.pd['to'], 'filter_id' : int(self.res['result'], 16)}
                res_datastore = phantomdb.store_filter(store)
                if not self.res_datastore:
                    return self.error_msg.error_response("err_store_data")
                
                try:
                    self.client = IPC_Client.Client()
                    self.res = self.client.send_message(self.pd)
                    return self.res
                except Exception as e:
                    return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("missing_params")


    def get_shh_messages(self,postparams):
    
        if len(postparams['params']) == 1:
            if postparams['params'][0] == "latest_filter":
                self.phantomdb = Phantom_Db.PhantomDb()
                self.res = self.phantomdb.get_latest_filter()
            
                if self.res == False:
                    return self.error_msg.error_response("err_select_data")
                if len(self.res) == 0:
                    return self.error_msg.error_response("no_filters")

                """ By now "res" will always contain a list of tuples that it got from sqlite3 """
                self.filter_id = hex(self.res[0][0])

            else:
                try:
                    self.filter_id = hex(int(postparams['params'][0]))
                except:
                    return self.error_msg.error_response("invalid_parameters")
            
            try:
                self.client = IPC_Client.Client()
                self.res = self.client.get_shh_messages(filter_id)
                return self.res
            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("missing_params")


    def get_transaction_history(self,postparams):
    
        if len(postparams['params']) == 1:

            if not self.verify_wallet_addr(postparams['params'][0]):
                return self.error_msg.error_response("invalid_wallet_addr")

            try:
                self.phantomdb = Phantom_Db.PhantomDb()
                self.res = self.phantomdb.get_transaction_hist(postparams['params'][0][2:])
                if self.res and len(self.res) >= 1:
                    return {"jsonrpc": "2.0", "id": "1", "result": list(self.res)}
                return {"jsonrpc": "2.0", "id": "1", "result": []}
            except Exception as e:
                return self.error_msg.error_response("err_trans_hist")
        return self.error_msg.error_response("missing_params")


    def store_address_book(self,postparams):
    
        if len(postparams['params']) == 2:

            if not self.verify_wallet_addr(postparams['params'][0]):
                return self.error_msg.error_response("invalid_wallet_addr")

            if len(postparams['params'][1]) > 0:
                try:
                    self.phantomdb = Phantom_Db.PhantomDb()
                    self.res = self.phantomdb.store_address_book(postparams['params'][0][2:], postparams['params'][1])
                    if self.res:
                        return {"jsonrpc": "2.0", "id": "1", "result": ["true"]}
                except Exception as e:
                    return self.error_msg.error_response("err_store_addrbook")
        return self.error_msg.error_response("missing_params")


    def del_address_book(self,postparams):
    
        if len(postparams['params']) == 1:

            if not self.verify_wallet_addr(postparams['params'][0]):
                return self.error_msg.error_response("invalid_wallet_addr")

            try:
                self.phantomdb = Phantom_Db.PhantomDb()
                self.res = self.phantomdb.del_address_book(postparams['params'][0][2:])
                if self.res:
                    return {"jsonrpc": "2.0", "id": "1", "result": ["true"]}
            except Exception as e:
                return self.error_msg.error_response("err_del_addrbook")
        return self.error_msg.error_response("missing_params")


    def get_address_book(self,postparams):
    
        if len(postparams['params']) == 0:
            try:
                self.phantomdb = Phantom_Db.PhantomDb()
                self.res = self.phantomdb.get_address_book()
                if self.res and len(self.res) >= 1:
                    return {"jsonrpc": "2.0", "id": "1", "result": list(self.res)}
                return {"jsonrpc": "2.0", "id": "1", "result": []}
            except Exception as e:
                return self.error_msg.error_response("err_addr_book")
        return self.error_msg.error_response("no_params_allowed")


    def get_balance_by_block(self,postparams):
    
        if len(self.postparams['params']) == 2:

            if not self.verify_wallet_addr(postparams['params'][0]):
                return self.error_msg.error_response("invalid_wallet_addr")

            if type(self.postparams['params'][1]) is not list:
                return self.error_msg.error_response("missing_params")

            try:
                self.phantomdb = Phantom_Db.PhantomDb()
                self.results = []

                for block_number in postparams['params'][1]:
                    if type(postparams['params'][1][0]) is not int:
                        return self.error_msg.error_response("invalid_block_number")

                    self.res = self.phantomdb.get_balance_by_block(postparams['params'][0],block_number)
                    if self.res and len(self.res) >= 1:
                        self.results.append(self.res)
            except Exception as e:
                return self.error_msg.error_response("err_get_balance_block")

            return {"jsonrpc": "2.0", "id": "1", "result": self.results}
        return self.error_msg.error_response("missing_params")


    def create_contract(self, postparams):

        if len(postparams['params']) == 1 and len(postparams['params'][0]) == 4:

            if 'from_account' in postparams['params'][0]:
                if not self.verify_wallet_addr(postparams['params'][0]['from_account']):
                    return self.error_msg.error_response("invalid_wallet_addr")

            else:
                return self.error_msg.error_response("missing_params")

            """ Source is the compiled EVM source of the contract. """
            if not 'source' in postparams['params'][0] or not len(postparams['params'][0]['source']) > 0:
                return self.error_msg.error_response("missing_params")

            """ Since we do not estimate the gas needed for the contract to be create, every user must specify the amount of gas. """
            if not 'gas' in postparams['params'][0] or not len(postparams['params'][0]['gas']) > 0:
                return self.error_msg.error_response("missing_params")
        
            """ Password is needed to unlock the wallet and pay for the gas. """
            if not 'password' in postparams['params'][0] or not len(postparams['params'][0]['password']) > 0:
                return self.error_msg.error_response("empty_password")

            self.from_addr = postparams['params'][0]['from_account']
            self.source = postparams['params'][0]['source']
            self.gas = postparams['params'][0]['gas']
            self.passwd = postparams['params'][0]['password']

            try:
                from Contract.Contract import ContractCall
                self.contract = ContractCall()
                self.contract_tx = self.contract.create_contract(self.from_addr, self.source, self.gas, self.passwd)
                return {"jsonrpc": "2.0", "id": "1", "result": self.contract_tx}
            except Exception as e:
                return {"jsonrpc": "2.0", "id": "1", "result": e}
        return self.error_msg.error_response("missing_params")


    def set_contract_storage(self, postparams):

        if len(postparams['params']) == 1 and len(postparams['params'][0]) == 6:
            if 'from' in postparams['params'][0] and 'to' in postparams['params'][0] \
                and 'function_signature' in postparams['params'][0] and 'function_argument' in postparams['params'][0] and \
                    'password' in postparams['params'][0] and 'gas' in postparams['params'][0]:

                if not self.verify_wallet_addr(postparams['params'][0]['from']):
                    return self.error_msg.error_response("invalid_wallet_addr")

                if not self.verify_wallet_addr(postparams['params'][0]['to']):
                    return self.error_msg.error_response("invalid_wallet_addr")

                if not len(postparams['params'][0]['function_signature']) > 0:
                    return self.error_msg.error_response("no_function_sign")

                if not len(postparams['params'][0]['password']) > 0:
                    return self.error_msg.error_response("empty_password")

                if not len(postparams['params'][0]['gas']) > 0:
                    return self.error_msg.error_response("err_gas")

                try:
                    from Contract.Contract import ContractCall
                    self.contract = ContractCall()
                    """ from_addr, contract_addr, 'set_s(string)', ['Hello, world'] """
                    self.contract_call_res = self.contract.call_with_transaction(postparams['params'][0])
                    return {"jsonrpc": "2.0", "id": "1", "result": self.contract_call_res}
                except Exception as e:
                    print e
                    return {"jsonrpc": "2.0", "id": "1", "result": e}
        return self.error_msg.error_response("missing_params")


    def get_contract_storage(self, postparams):

        if 'function_signature' in postparams['params'][0] and 'to' in postparams['params'][0] and \
            'function_argument' in postparams['params'][0] and 'return_type' in postparams['params'][0]:

            if not self.verify_wallet_addr(postparams['params'][0]['to']):
                return self.error_msg.error_response("invalid_wallet_addr")

            if not len(postparams['params'][0]['function_signature']) > 0:
                return self.error_msg.error_response("no_function_sign")

            """ TODO: validate more return types. """
            if not postparams['params'][0]['return_type'][0] == 'string':
                return self.error_msg.error_response("no_return_type")
            
            pd = postparams['params'][0]

            from Contract.Contract import ContractCall
            self.contract = ContractCall()

            """ to_address (string), function signature(string), function argument(s)(list of strings), 
                return type(s)(list of strings) """
            res = self.contract.call(pd['to'], pd['function_signature'], pd['function_argument'], pd['return_type'])
            return res
        return self.error_msg.error_response("missing_params")


    def call(self, postparams):

        if 'to' in postparams['params'][0] and 'data' in postparams['params'][0]:

            if not self.verify_wallet_addr(postparams['params'][0]['to']):
                return self.error_msg.error_response("invalid_wallet_addr")

            try:
                self.client = IPC_Client.Client()
                pd = postparams['params'][0]
                res = self.client.call(pd)
                return res
            except Exception as e:
                print e
                return {"jsonrpc": "2.0", "id": "1", "result": e}
        return self.error_msg.error_response("missing_params")



    def create_static_nodefile(self):

        self.client = IPC_Client.Client()
        if self.client.create_static_nodefile():
            pass
        else:
            pass

    def get_tx_receipt(self, postparams):
        
        if len(postparams['params']) == 1:
            self.client = IPC_Client.Client()
            try:
                txrec = self.client.get_tx_reciept(postparams['params'][0])
                if 'result' in txrec:
                    return txrec
                return {"jsonrpc": "2.0", "id": "1", "result": "false"}
            except Exception as e:
                return self.error_msg.error_response("err_get_txrec")
        return self.error_msg.error_response("missing_params")
  

    def run(self,postdata):
        self.res = self.validate_postdata(postdata)

        if 'result' in self.res and self.res['result'][0] == "false":
            return self.res
        self.http_response = self.run_method.execute(self.res)
        return self.http_response
