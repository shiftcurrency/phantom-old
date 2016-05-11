import Phantom_Ui
import Error_Msg

def execute(postparams):

    if postparams['method'] == 'get_shiftbase':
        res = Phantom_Ui.get_shiftbase(postparams)
        return res
    
    elif postparams['method'] == 'rr_ptr':
        res = Phantom_Ui.rr_ptr(postparams)
        return res

    elif postparams['method'] == 'unlock_account':
        if 'params' in postparams and len(postparams['params']) == 2:
            res = Phantom_Ui.unlock_account(postparams['params'][0], postparams['params'][1])
            return res
        return Error_Msg.error_response("missing_params")

    elif postparams['method'] == 'lock_account':
        if 'params' in postparams and len(postparams['params']) == 1:
            res = Phantom_Ui.lock_account(postparams['params'][0])
            return res
        return Error_Msg.error_response("missing_params")

    elif postparams['method'] == 'create_site':
        res = Phantom_Ui.create_site(postparams)
        return res

    elif postparams['method'] == 'create_account':
        res = Phantom_Ui.create_account(postparams)
        return res

    elif postparams['method'] == 'send_transaction':
        res = Phantom_Ui.send_transaction(postparams)
        return res

    elif postparams['method'] == 'send_rawtransaction':
        res = Phantom_Ui.send_rawtransaction(postparams)
        return res

    elif postparams['method'] == 'get_accounts':
        res = Phantom_Ui.get_accounts(postparams)
        return res

    elif postparams['method'] == 'net_peercount':
        res = Phantom_Ui.get_peercount(postparams)
        return res

    elif postparams['method'] == 'net_listening':
        res = Phantom_Ui.net_listening(postparams)
        return res
    
    elif postparams['method'] == 'get_blocknumber':
        res = Phantom_Ui.get_blocknumber(postparams)
        return res

    elif postparams['method'] == 'sign_and_publish':
        res = Phantom_Ui.sign_publish_site(postparams)
        return res

    elif postparams['method'] == 'get_blockdata':
        res = Phantom_Ui.get_block_data(postparams)
        return res

    elif postparams['method'] == 'get_balance':
        res = Phantom_Ui.get_balance(postparams)
        return res

    elif postparams['method'] == 'new_message_ident':
        res = Phantom_Ui.new_message_ident(postparams)
        return res

    elif postparams['method'] == 'message_ident_exists':
        res = Phantom_Ui.message_ident_exists(postparams)
        return res

    return Error_Msg.error_response("no_method")
