import json
import Error_Msg
import Run_Method
from Shift_IPC import IPC_Client
import Phantom_Db


def create_phantom_site():

    from Config import config
    from Crypt import CryptBitcoin
    from Site import Site
    import os

    config.parse(silent=True)
    if not config.arguments:
        config.parse()

    privatekey = CryptBitcoin.newPrivatekey()
    address = CryptBitcoin.privatekeyToAddress(privatekey)

    try:
        os.mkdir("%s/%s" % (config.data_dir, address))
        open("%s/%s/index.html" % (config.data_dir, address), "w").write("Hello %s!" % address)
    except Exception as e:
        return Error_Msg.error_response("err_create_sitedir")
    
    try:
        site = Site(address)
        site.content_manager.sign(privatekey=privatekey, extend={"postmessage_nonce_security": True})
        site.settings["own"] = True
        site.saveSettings()
    except Exception as e:
        return Error_Msg.error_response("err_create_site")

    return {"jsonrpc": "2.0", "id": "1", "result": ["true", str(address), str(privatekey)]}
        

def validate_postdata(postdata):

    try:
        """ 
        Convert the HTTP body json string into a dictionary. A non valid json string will return false.
        """
        postparams = json.loads(postdata)
    except Exception as e:
        return Error_Msg.error_response("invalid_json_req")

    if 'jsonrpc' in postparams and not postparams['jsonrpc'] == '2.0':
        return Error_Msg.error_response("invalid_json_ver")

    if 'method' in postparams and len(postparams['method']) == 0:
        return Error_Msg.error_response("no_method")

    if not 'params' in postparams:
        return Error_Msg.error_response("missing_params")

    return postparams


def run_method(postparams):

    res = Run_Method.execute(postparams)
    return res


def get_shiftbase(postparams):

    if len(postparams['params']) == 0:
        try:
            client = IPC_Client.Client()
            res = client.get_shiftbase()
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")
    return Error_Msg.error_response("no_params_allowed")


def get_peercount(postparams):
    
    if len(postparams['params']) == 0:
        try:
            client = IPC_Client.Client()
            res = client.get_peercount()
            if 'result' in res:
                res['result'] = str(int(res['result'], 16))
            return res

        except Exception as e:
            print e
            return Error_Msg.error_response("ipc_call_error")
    return Error_Msg.error_response("no_params_allowed")



def get_blocknumber(postparams):
    
    if len(postparams['params']) == 0:
        try:
            client = IPC_Client.Client()
            res = client.get_blocknumber()
            if 'result' in res:
                res['result'] = str(int(res['result'], 16))
            return res 

        except Exception as e:
            print e
            return Error_Msg.error_response("ipc_call_error")
    return Error_Msg.error_response("no_params_allowed")


def get_block_data(postparams):

    if len(postparams['params']) == 2:
        if postparams['params'][1] == "true" or postparams['params'][1] == "false":
            try:
                client = IPC_Client.Client()
                res = client.get_block_data(postparams['params'][0], postparams['params'][1])
                return res
            except Exception as e:
                return Error_Msg.error_response("ipc_call_error")
        return Error_Msg.error_response("invalid_parameters")
    return Error_Msg.error_response("missing_params")


def rr_ptr(postparams):

    if len(postparams['params']) == 1:
        if not postparams['params'][0][:-6].isalnum() and not postparams[param].endswith('.shift'):
            return Error_Msg.error_response("invalid_domain")
        else:
            pass

    return Error_Msg.error_response("")


def get_accounts(postparams):

    if len(postparams['params']) == 0:
        try:
            client = IPC_Client.Client()
            res = client.get_accounts()
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")
    return Error_Msg.error_response("no_params_allowed")


def get_balance(postparams):

    if len(postparams['params']) == 2:
        addr = postparams['params'][0]
        when = postparams['params'][1]

        try:
            int(addr, 16) 
        except ValueError as e:
            return Error_Msg.error_response("invalid_wallet_addr")

        if when == "latest" or when == "pending" or when == "earliest":

            try:
                client = IPC_Client.Client()
                res = client.get_balance(addr, when)
                if 'result' in res:
                    res['result'] = str(int(res['result'], 16))
                return res
            except Exception as e:
                return Error_Msg.error_response("ipc_call_error")
    return Error_Msg.error_response("missing_params")
            
 

def sign_publish_site(self, postparams):

    from Site import Site

    if not len(postparams['params']) == 2 and not len(postparams['params'][0]) == 34:
        return Error_Msg.error_response("sign_missing_params")

    address = postparams['params'][0]
    privatekey = postparams['params'][1]

    site = Site(address, allow_create=False)
    try:
        success = site.content_manager.sign(inner_path="content.json", privatekey=privatekey, update_changed_files=True)
        if success:
            self.sitePublish(address, inner_path=inner_path)
    except Exception as e:
        return Error_Msg.error_response("err_sign_site")
        

    return {"jsonrpc": "2.0", "id": "1", "result": ["true", str(address)]}



def unlock_account(addr, password):

    try:
        int(addr, 16)
    except ValueError as e:
        return Error_Msg.error_response("invalid_wallet_addr")

    if not len(addr) == 42:
        return Error_Msg.error_response("invalid_wallet_addr")

    elif not len(password) > 0:
        return Error_Msg.error_response("empty_password")

    else:
        try:
            client = IPC_Client.Client()
            res = client.unlock_account(addr, password)
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")


def lock_account(addr):

    try:
        int(addr, 16)
    except ValueError as e:
        return Error_Msg.error_response("invalid_wallet_addr")

    try:
        client = IPC_Client.Client()
        res = client.lock_account(addr)
        return res
    except Exception as e:
        return Error_Msg.error_response("ipc_call_error")


def create_site(postparams):

    if len(postparams['params']) == 0:
        return create_phantom_site()

    return Error_Msg.error_response("")


def create_account(postparams):

    if len(postparams['params']) == 1:
        if len(postparams['params'][0]) == 0:
            return Error_Msg.error_response("empty_password")
        try:
            client = IPC_Client.Client()
            res = client.create_account(postparams['params'][0])
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")


def net_listening(postparams):

    if len(postparams['params']) == 0:
        try:
            client = IPC_Client.Client()
            res = client.net_listening()
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")
    return Error_Msg.error_response("no_params_allowed")


def send_transaction(postparams):

    if len(postparams['params']) == 1:
        pd = postparams['params'][0]
        try:
            int(pd['from'], 16)
            int(pd['to'], 16)
        except ValueError as e:
            return Error_Msg.error_response("invalid_wallet_addr")

        if not len(pd['from']) == 42 or not len(pd['to']) == 42:
            Error_Msg.error_response("invalid_wallet_addr")

        try:
            int(pd['amount'])
        except Exception as e:
            return Error_Msg.error_response("invalid_amount")

        if 'data' in pd and len(pd['data']) > 0: data = pd['data']
        else: data = False

        if 'nrg' in pd and len(pd['nrg']) > 0: nrg = pd['nrg']
        else: nrg = False

        client = IPC_Client.Client()

        if 'password' in pd and len(pd['password']) == 0:
            return Error_Msg.error_response("empty_password")
        else:
            res = client.unlock_account(pd['from'], pd['password'])

        try:
            res = client.send_transaction(pd['from'], pd['to'], pd['amount'], nrg, data)
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")


def send_rawtransaction(postparams):

    if len(postparams['params']) == 1:
        try:
            int(postparams['params'][0], 16)
        except Exception as e:
            Error_Msg.error_response("invalid_hex_string")
        
        try:
            res = client.send_transaction(postparams['params'][0])
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")
    return Error_Msg.error_response("invalid_parameters")


def create_shh_filter(postparams):

    if len(postparams['params']) == 1:
        pd = postparams['params'][0]
        if 'to' in pd and 'topics' in pd:
            try:
                int(pd['to'], 16)
            except:
                return Error_Msg.error_response("invalid_hex_string")

            if pd['topics'] == "":
                return Error_Msg.error_response("err_create_filter")
            params = {"to": str(pd['to']), "topics": [str(pd['topics'][0].encode("hex"))]}
            client = IPC_Client.Client()
            try:
                res = client.create_shh_filter(params)
                return res
            except Exception as e:
                return Error_Msg.error_response("ipc_call_error")
    return Error_Msg.error_response("missing_params")


def new_message_ident(postparams):

    if len(postparams['params']) == 0:
        client = IPC_Client.Client()
        try:
            res = client.new_message_ident()
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")
    return Error_Msg.error_response("no_params_allowed")


def message_ident_exists(postparams):
    if len(postparams['params']) == 1:
        try:
            int(postparams['params'][0], 16)
        except:
            Error_Msg.error_response("invalid_hex_string")

        client = IPC_Client.Client()
        try:
            res = client.message_ident_exists(postparams['params'][0])
            return res 
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")
    return Error_Msg.error_response("missing_params")


def send_message(postparams):

    if len(postparams['params']) == 1:
        pd = postparams['params'][0]

        if 'to' in pd and 'message' in pd and pd['message'] != "":
            try:
                int(pd['to'], 16)
            except:
                Error_Msg.error_response("invalid_hex_string")

            from_ident = new_message_ident({'params':''})
            if 'result' in from_ident and len(from_ident['result']) == 2:
                return Error_Msg.error_response("err_gen_ident")

            pd['from'] = from_ident['result']
            pd['topics'] = ['{"type":"c","store-encrypted":"true"}'.encode("hex")]
            pd['priority'] = "0x64"
            pd['ttl'] = "0x64"
            pd['message'] = pd['message'].encode("hex")

            """ Create filter to wait for incoming answers. Use postparams with the unhexed strings. """
            res  = create_shh_filter(postparams)

            try:
                int(res['result'], 16)
            except:
                return Error_Msg.error_response("err_create_filter")

            phantomdb = Phantom_Db.PhantomDb()
            store = {'to':pd['to'], 'filter_id' : int(res['result'], 16)}
            res_datastore = phantomdb.store_data(store)
            if not res_datastore:
                return Error_Msg.error_response("err_store_data")
                
            try:
                client = IPC_Client.Client()
                res = client.send_message(pd)
                return res
            except Exception as e:
                return Error_Msg.error_response("ipc_call_error")
    return Error_Msg.error_response("missing_params")


def get_shh_messages(postparams):
    
    if len(postparams['params']) == 1:
        if postparams['params'][0] == "latest_filter":
            phantomdb = Phantom_Db.PhantomDb()
            res = phantomdb.get_latest_filter()
            
            if res == False:
                return Error_Msg.error_response("err_select_data")
            if len(res) == 0:
                return Error_Msg.error_response("no_filters")

            """ By now "res" will always contain a list of tuples that it got from sqlite3 """
            filter_id = hex(res[0][0])

        else:
            try:
                filter_id = hex(int(postparams['params'][0]))
            except:
                return Error_Msg.error_response("invalid_parameters")
            
        try:
            client = IPC_Client.Client()
            res = client.get_shh_messages(filter_id)
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")
    return Error_Msg.error_response("missing_params")


def run(postdata):
    res = validate_postdata(postdata)

    if 'result' in res and res['result'][0] == "false":
        return res
    http_response = run_method(res)
    return http_response
