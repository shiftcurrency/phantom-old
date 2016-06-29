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

        self.config.parse(silent=True)
        if not self.config.arguments:
            self.config.parse()

        self.privatekey = CryptBitcoin.newPrivatekey()
        address = CryptBitcoin.privatekeyToAddress(self.privatekey)

        try:
            os.mkdir("%s/%s" % (self.config.data_dir, address))
            open("%s/%s/index.html" % (self.config.data_dir, address), "w").write("Hello %s!" % address)
        except Exception as e:
            return self.error_msg.error_response("err_create_sitedir")
    
        try:
            self.site = Site(address)
            self.site.content_manager.sign(privatekey=self.privatekey, extend={"postmessage_nonce_security": True})
            self.site.settings["own"] = True
            self.site.saveSettings()
        except Exception as e:
            return self.error_msg.error_response("err_create_site")
        return {"jsonrpc": "2.0", "id": "1", "result": ["true", str(address), str(privatekey)]}


    def validate_postdata(self,postdata):

        print postdata

        try:
            """ 
            Convert the HTTP body json string into a dictionary. A non valid json string will return false.
            """
            postparams = json.loads(postdata)
        except Exception as e:
            return self.error_msg.error_response("invalid_json_req")

        if 'jsonrpc' in postparams and not postparams['jsonrpc'] == '2.0':
            return self.error_msg.error_response("invalid_json_ver")

        if 'method' in postparams and len(postparams['method']) == 0:
            return self.error_msg.error_response("no_method")

        if not 'params' in postparams:
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

            try:
                int(self.addr, 16) 
            except ValueError as e:
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

        try:
            int(addr, 16)
        except ValueError as e:
            return self.error_msg.error_response("invalid_wallet_addr")

        if not len(addr) == 42:
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

        try:
            int(addr, 16)
        except ValueError as e:
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


    def send_transaction(self,postparams):

        if len(postparams['params']) == 1:
            self.self.pd = postparams['params'][0]
            try:
                int(self.self.pd['from'], 16)
                int(self.self.pd['to'], 16)
            except ValueError as e:
                return self.error_msg.error_response("invalid_wallet_addr")

            if not len(self.self.pd['from']) == 42 or not len(self.self.pd['to']) == 42:
                self.error_msg.error_response("invalid_wallet_addr")

            try:
                self.self.pd['amount'] = int(float(self.self.pd['amount'])*1000000000000000000)
                self.amount = "0x" + format(self.self.pd['amount'], 'x')
            except Exception as e:
                return self.error_msg.error_response("invalid_amount")

            if 'data' in self.self.pd and len(self.self.pd['data']) > 0: self.data = self.self.pd['data']
            else: self.data = False

            if 'nrg' in self.self.pd and len(self.self.pd['nrg']) > 0: self.nrg = self.self.pd['nrg']
            else: self.nrg = False

            self.client = IPC_Client.Client()

            if 'password' in self.self.pd and len(self.self.pd['password']) == 0:
                return self.error_msg.error_response("empty_password")
            else:
                self.res = self.client.unlock_account(self.self.pd['from'], self.self.pd['password'])

            try:
                self.res = self.client.send_transaction(self.self.pd['from'], self.self.pd['to'], self.amount, self.nrg, self.data)
            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")

            return self.res

    def send_rawtransaction(self,postparams):

        if len(postparams['params']) == 1:
            try:
                int(postparams['params'][0], 16)
            except Exception as e:
                self.error_msg.error_response("invalid_hex_string")
        
            try:
                self.res = self.client.send_transaction(postparams['params'][0])
                return res
            except Exception as e:
                return self.error_msg.error_response("ipc_call_error")
        return self.error_msg.error_response("invalid_parameters")


    def create_shh_filter(self,postparams):
    
        if len(postparams['params']) == 1:
            self.self.pd = postparams['params'][0]
            if 'to' in self.self.pd and 'topics' in self.pd:
                try:
                    int(self.pd['to'], 16)
                except:
                    return self.error_msg.error_response("invalid_hex_string")

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
            self.client = self.IPC_Client.Client()
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
                self.error_msg.error_response("invalid_hex_string")

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
                try:
                    int(self.pd['to'], 16)
                except:
                    self.error_msg.error_response("invalid_hex_string")

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

                self.phantomdb = self.Phantom_Db.PhantomDb()
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
            try:
                int(postparams['params'][0], 16)
            except:
                self.error_msg.error_response("invalid_hex_string")

            if not len(postparams['params'][0]) == 42: 
                self.error_msg.error_response("invalid_wallet_addr")

            try:
                self.phantomdb = Phantom_Db.PhantomDb()
                self.res = self.phantomdb.get_transaction_hist(postparams['params'][0])
                if self.res and len(self.res) >= 1:
                    return {"jsonrpc": "2.0", "id": "1", "result": list(self.res)}
                return {"jsonrpc": "2.0", "id": "1", "result": []}
            except Exception as e:
                return self.error_msg.error_response("err_trans_hist")
        return self.error_msg.error_response("missing_params")


    def store_address_book(self,postparams):
    
        if len(postparams['params']) == 2:
            try:
                int(postparams['params'][0], 16)
            except:
                self.error_msg.error_response("invalid_hex_string")

            if not len(postparams['params'][0]) == 42: 
                self.error_msg.error_response("invalid_wallet_addr")

            if len(postparams['params'][1]) > 0:
                try:
                    self.phantomdb = Phantom_Db.PhantomDb()
                    self.res = self.phantomdb.store_address_book(postparams['params'][0], postparams['params'][1])
                    if res:
                        return {"jsonrpc": "2.0", "id": "1", "result": ["true"]}
                except Exception as e:
                    return self.error_msg.error_response("err_store_addrbook")
        return self.error_msg.error_response("missing_params")


    def del_address_book(self,postparams):
    
        if len(postparams['params']) == 1:
            try:
                int(postparams['params'][0], 16)
            except:
                self.error_msg.error_response("invalid_hex_string")

            if not len(postparams['params'][0]) == 42:
                self.error_msg.error_response("invalid_wallet_addr")

            try:
                self.phantomdb = Phantom_Db.PhantomDb()
                self.res = phantomdb.del_address_book(postparams['params'][0])
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

            try:
                int(self.postparams['params'][0], 16)
            except:
                self.error_msg.error_response("invalid_hex_string")

            if not len(self.postparams['params'][0]) == 42:
                self.error_msg.error_response("invalid_wallet_addr")

            if type(self.postparams['params'][1]) is not list:
                return self.error_msg.error_response("missing_params")

            try:
                self.phantomdb = Phantom_Db.PhantomDb()
                self.results = []

                for block_number in postparams['params'][1]:
                    if type(postparams['params'][1][0]) is not int:
                        self.error_msg.error_response("invalid_block_number")

                    self.res = self.phantomdb.get_balance_by_block(postparams['params'][0],block_number)
                    if self.res and len(self.res) >= 1:
                        self.results.append(self.res)
            except Exception as e:
                return self.error_msg.error_response("err_get_balance_block")

            return {"jsonrpc": "2.0", "id": "1", "result": self.results}
        return self.error_msg.error_response("missing_params")


    def create_static_nodefile(self):

        self.client = IPC_Client.Client()
        if self.client.create_static_nodefile():
            pass
        else:
            pass
  

    def run(self,postdata):
        self.res = self.validate_postdata(postdata)

        if 'result' in self.res and self.res['result'][0] == "false":
            return self.res
        self.http_response = self.run_method.execute(self.res)
        return self.http_response
