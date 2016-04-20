import Shift_Ui

def execute(postparams):

    if postparams['method'] == 'get_shiftbase':
        res = Shift_Ui.get_shiftbase(postparams)
        return res
    
    elif postparams['method'] == 'rr_ptr':
        res = Shift_Ui.rr_ptr(postparams)
        return res

    elif postparams['method'] == 'unlock_account':
        res = Shift_Ui.unlock_account(postparams)
        return res

    elif postparams['method'] == 'create_site':
        res = Shift_Ui.create_site(postparams)
        return res

    elif postparams['method'] == 'create_account':
        res = Shift_Ui.create_account(postparams)
        return res

    elif postparams['method'] == 'send_transaction':
        res = Shift_Ui.send_transaction(postparams)
        return res

    elif postparams['method'] == 'get_accounts':
        res = Shift_Ui.get_accounts(postparams)
        return res

    elif postparams['method'] == 'get_peercount':
        res = Shift_Ui.get_peercount(postparams)
        return res
    
    elif postparams['method'] == 'get_blocknumber':
        res = Shift_Ui.get_blocknumber(postparams)
        return res

    elif postparams['method'] == 'sign_and_publish':
        res = Shift_Ui.sign_publish_site(postparams)
        return res

    return Error_Msg.error_response("no_method")
