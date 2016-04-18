import json
import Error_Msg
from Shift_IPC import IPC_Client


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

    print postparams

    client = IPC_Client.Client()

    if postparams['method'] == 'get_shiftbase':
        res = get_shiftbase(postparams)
        return res
    
    elif postparams['method'] == 'rr_ptr':
        res = rr_ptr(postparams)
        return res

    elif postparams['method'] == 'unlock_account':
        res = unlock_account(postparams)
        return res

    elif postparams['method'] == 'create_site':
        res = create_site(postparams)
        return res

    elif postparams['method'] == 'create_account':
        res = create_account(postparams)
        return res

    elif postparams['method'] == 'send_transaction':
        res = send_transaction(postparams)
        return res


def get_shiftbase(postparams):

    if len(postparams['params']) == 0:
        
        try:
            res = client.get_shiftbase()
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")


def rr_ptr(postparams):

    if len(postparams['params']) == 1:
        if not postparams['params'][0][:-6].isalnum() and not postparams[param].endswith('.shift'):
            return Error_Msg.error_response("invalid_domain")
        else:
            pass


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
            res = client.unlock_account(addr, password)
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")


def create_site(postparams):

    if len(postparams['params']) == 0:
        return create_phantom_site()


def create_account(postparams):

    if len(postparams['params']) == 1:
        if len(postparams['params'][0]) < 0:
            return Error_Msg.error_response("empty_password")
        try:
            res = client.create_account(postparams['params'][0])
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")


def send_transaction(postparams):

    if len(postparams['params']) == 1:

        pd = postparams['params'][0]
        client = IPC_Client.Client()
        
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

        if 'data' in pd and len(pd['data']) > 0:
            data = pd['data']
        else:
            data = False

        if 'nrg' in pd and len(pd['nrg']) > 0:
            nrg = pd['nrg']
        else:
            nrg = False

        if 'password' in pd and len(pd['password']) == 0:
            Error_Msg.error_response("empty_password")
        else:
            res = client.unlock_account(pd['from'], pd['password'])

        try:
            res = client.send_transaction(pd['from'], pd['to'], pd['amount'], nrg, data)
            return res
        except Exception as e:
            return Error_Msg.error_response("ipc_call_error")


def run(postdata):
    res = validate_postdata(postdata)

    if 'result' in res and res['result'][0] == "false":
        return res

    http_response = run_method(res)
    return http_response
