import socket
import json
import os
import sys

class Client(object):

    def __init__(self, ipc_path=None, *args, **kwargs):
        if ipc_path is None:
            ipc_path = self.get_default_ipc_path()

        self.ipc_path = ipc_path
        self._socket = self.get_socket()

        super(Client, self).__init__(*args, **kwargs)


    def get_shiftbase(self):
        response = self._make_request("shf_shiftbase", [])
        return response


    def unlock_account(self, account, password):
        response = self._make_request("personal_unlockAccount", [account,password,60])
        return response

    def lock_account(self, account):
        """ Method not implemented ? """
        response = self._make_request("personal_lockAccount", [account])
        return response

    def create_account(self, password):
        response = self._make_request("personal_newAccount", [password])
        return response

    def get_accounts(self):
        response = self._make_request("shf_accounts", [])
        return response

    def get_peercount(self):
        response = self._make_request("net_peerCount", [])
        return response

    def net_listening(self):
        response = self._make_request("net_listening", [])
        return response

    def get_blocknumber(self):
        response = self._make_request("shf_blockNumber", [])
        return response

    def get_balance(self, account, when):
        response = self._make_request("shf_getBalance", [account,when])
        return response

    def new_message_ident(self):
        response = self._make_request("shh_newIdentity", [])
        return response

    def message_ident_exists(self, ident):
        response = self._make_request("shh_hasIdentity", [ident])
        return response

    def send_message(self, params):
        response = self._make_request("shh_post", [params])
        return response

    def create_shh_filter(self, params):
        response = self._make_request("shh_newFilter", [params])
        return response

    def get_shh_messages(self, params):
        response = self._make_request("shh_getFilterChanges"):
        return response

    def get_block_data(self, blknum, fulldata):
        if fulldata == "true":
            response = self._make_request("shf_getBlockByNumber", [hex(int(blknum)), True])
        else:
            response = self._make_request("shf_getBlockByNumber", [hex(int(blknum)), False])
            
        return response


    def send_transaction(self, sender, receiver, amount, nrg, data):

        if nrg and not data:
            trans_params = [{"from": sender, "to": receiver, "value": hex(int(amount)), "gas": hex(int(nrg))}]
        elif nrg and data:
            trans_params = [{"from": sender, "to": receiver, "value": hex(int(amount)), "gas": hex(int(nrg)), "data" : data}]
        else:
            trans_params = [{"from": sender, "to": receiver, "value": hex(int(amount))}]

        response = self._make_request("shf_sendTransaction", trans_params)
        return response

    def send_rawtransaction(self, data):
        response = self._make_request("shf_sendRawTransaction", data)
        return response


    def construct_json_request(self, method, params):
        request = json.dumps({"jsonrpc": "2.0","method": method, "params": params,"id": "1"})
        return request


    def get_default_ipc_path(self):

        ''' Return the path of shift IPC file depending on OS '''

        if sys.platform == 'darwin':
            ipc_path = os.path.expanduser("~/Library/gshift/gshift.ipc")
        elif sys.platform == 'linux2':
            ipc_path = os.path.expanduser("~/.gshift/gshift.ipc")
        elif sys.platform == 'win32':
            ipc_path = os.path.expanduser("\\~\\AppData\\Roaming\\gshift")
        else:
            raise ValueError(
                "Unsupported platform.  Only darwin/linux2/win32 are "
                "supported.  You must specify the ipc_path"
            )
        return ipc_path


    def get_socket(self):
        try:
            _socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            _socket.connect(self.ipc_path)
            # Tell the socket not to block on reads.
            """ Two seconds seems to be enough. One second is not enough when creating accounts """
            _socket.settimeout(2)
            return _socket
        except Exception as e:
            return False

            


    def _make_request(self, method, params):
        request = self.construct_json_request(method, params)
        
        for _ in range(3):
            self._socket.sendall(request)
            response_raw = ""

            while True:
                try:
                    response_raw += self._socket.recv(4096)
                except socket.timeout:
                    break

            if response_raw == "":
                self._socket.close()
                self._socket = self.get_socket()
                continue

            break
        else:
            raise ValueError("No JSON returned by socket")

        response = json.loads(response_raw)

        if "error" in response:
            raise ValueError(response["error"]["message"])

        return response
