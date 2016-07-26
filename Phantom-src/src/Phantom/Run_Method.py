import Phantom_Ui
import Error_Msg

class Run_Method(object):

    def execute(self,postparams):

        phantom_ui = Phantom_Ui.Phantom_Ui()
        error = Error_Msg.Error_Msg()

        if postparams['method'] == 'get_shiftbase':
            self.res = phantom_ui.get_shiftbase(postparams)
            return self.res
    
        elif postparams['method'] == 'rr_ptr':
            self.res = phantom_ui.rr_ptr(postparams)
            return self.res

        elif postparams['method'] == 'unlock_account':
            if 'params' in postparams and len(postparams['params']) == 2:
                self.res = phantom_ui.unlock_account(postparams['params'][0], postparams['params'][1])
                return self.res
            return Error_Msg.error_self.response("missing_params")

        elif postparams['method'] == 'lock_account':
            if 'params' in postparams and len(postparams['params']) == 1:
                self.res = phantom_ui.lock_account(postparams['params'][0])
                return self.res
            return Error_Msg.error_self.response("missing_params")

        elif postparams['method'] == 'create_site':
            self.res = phantom_ui.create_site(postparams)
            return self.res

        elif postparams['method'] == 'create_account':
            self.res = phantom_ui.create_account(postparams)
            return self.res

        elif postparams['method'] == 'send_transaction':
            self.res = phantom_ui.send_transaction(postparams)
            return self.res

        elif postparams['method'] == 'send_rawtransaction':
            self.res = phantom_ui.send_rawtransaction(postparams)
            return self.res

        elif postparams['method'] == 'get_accounts':
            self.res = phantom_ui.get_accounts(postparams)
            return self.res

        elif postparams['method'] == 'net_peercount':
            self.res = phantom_ui.get_peercount(postparams)
            return self.res

        elif postparams['method'] == 'net_listening':
            self.res = phantom_ui.net_listening(postparams)
            return self.res
    
        elif postparams['method'] == 'get_blocknumber':
            self.res = phantom_ui.get_blocknumber(postparams)
            return self.res

        elif postparams['method'] == 'sign_and_publish':
            self.res = phantom_ui.sign_publish_site(postparams)
            return self.res

        elif postparams['method'] == 'get_blockdata':
            self.res = phantom_ui.get_block_data(postparams)
            return self.res

        elif postparams['method'] == 'get_balance':
            self.res = phantom_ui.get_balance(postparams)
            return self.res

        elif postparams['method'] == 'new_message_ident':
            self.res = phantom_ui.new_message_ident(postparams)
            return self.res

        elif postparams['method'] == 'message_ident_exists':
            self.res = phantom_ui.message_ident_exists(postparams)
            return self.res

        elif postparams['method'] == 'send_message':
            self.res = phantom_ui.send_message(postparams)
            return self.res

        elif postparams['method'] == 'create_shh_filter':
            self.res = phantom_ui.create_shh_filter(postparams)
            return self.res

        elif postparams['method'] == 'get_shh_messages':
            self.res = phantom_ui.get_shh_messages(postparams)
            return self.res

        elif postparams['method'] == 'get_transaction_history':
            self.res = phantom_ui.get_transaction_history(postparams)
            return self.res

        elif postparams['method'] == 'store_address_book':
            self.res = phantom_ui.store_address_book(postparams)
            return self.res

        elif postparams['method'] == 'del_address_book':
            self.res = phantom_ui.del_address_book(postparams)
            return self.res

        elif postparams['method'] == 'get_address_book':
            self.res = phantom_ui.get_address_book(postparams)
            return self.res

        elif postparams['method'] == 'get_balance_by_block':
            self.res = phantom_ui.get_balance_by_block(postparams)
            return self.res

        elif postparams['method'] == 'create_contract':
            self.res = phantom_ui.create_contract(postparams)
            return self.res

        elif postparams['method'] == 'get_tx_receipt':
            self.res = phantom_ui.get_tx_receipt(postparams)
            return self.res

        elif postparams['method'] == 'set_contract_storage':
            self.res = phantom_ui.set_contract_storage(postparams)
            return self.res

        elif postparams['method'] == 'get_contract_storage':
            self.res = phantom_ui.get_contract_storage(postparams)
            return self.res

        elif postparams['method'] == 'call':
            self.res = phantom_ui.call(postparams)
            return self.res

        return error.error_response("no_method")
