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


from ctypes import *
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
        response = self._make_request("personal_unlockAccount", [account,password,120])
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
        response = self._make_request("shh_getFilterChanges", [params])
        return response

    def get_tx_reciept(self, params):
        response = self._make_request("shf_getTransactionReceipt", [params])
        return response

    def get_block_data(self, blknum, fulldata):
        if fulldata == "true":
            response = self._make_request("shf_getBlockByNumber", [hex(int(blknum)), True])
        else:
            response = self._make_request("shf_getBlockByNumber", [hex(int(blknum)), False])
            
        return response

    def send_transaction(self, params):

        if params['method'] == 'send_transaction':
            trans_params = [{"from": params['from'], "to": params['to'], "value": params['amount'], "gas": hex(30000)}]
        elif params['method'] == 'create_contract':
            trans_params = [{"from": params['from'], "gas": hex(int(params['gas'])), "data" : params['data']}]
        elif params['method'] == 'call_contract':
            trans_params = [{"from": params['from'], "to" : params['to'], "gas": hex(int(params['gas'])), "data" : params['data']}]

        response = self._make_request("shf_sendTransaction", trans_params)
        return response

    def call(self, params):
        response = self._make_request("shf_call", [params, "latest"])
        return response

    def send_rawtransaction(self, data):
        response = self._make_request("shf_sendRawTransaction", data)
        return response

    def construct_json_request(self, method, params):
        request = json.dumps({"jsonrpc": "2.0","method": method, "params": params,"id": "1"})
        return request

    def create_static_nodefile(self):

        if not os.path.exists(self.get_default_node_path()):

            static_node_string = '["enode://4c8635f108dae8a997697d9c22ddca36969e7f9bc57d9fc01102d7e7d9633231331ae7f7307aceb1aa19130b5bdd4afe397db616c76e7ffc1c69302ba0d09a39@45.32.182.61:53900",' + \
                                  '"enode://80d0ce5c992f8cc83cdbfd6d832b2dff2e82fee1f8b58762cd858eaacfcc99d5a8a837648bd28a2d508cc1da305c15cf4e531546034ed1a8ccd07ff51a71abd6@108.61.177.0:53900",' + \
                                  '"enode://f019da062a635a4e9e89ec93edc7ca11c06fdfec0574f1cb001126a82dc6ffa6ca05f924a683934ff5d01fc5d4b0ac9507349a945c97121b2a355d39b1781cd7@104.238.157.156:53900"]'
            filepath = self.get_default_node_path()
            try:
                with open(filepath, 'w') as x:
                    x.write(static_node_string)
                x.close()
            except Exception as e:
                print e
                return False
        return True

    def get_default_node_path(self):

        ''' Return the path of the static node file depending on OS '''

        if sys.platform == 'darwin':
            node_path = os.path.expanduser("~/Library/gshift/static-nodes.json")
        elif sys.platform == 'linux2':
            node_path = os.path.expanduser("~/.gshift/static-nodes.json")
        elif sys.platform == 'win32':
            node_path = os.path.expanduser("~\AppData\Roaming\gshift\static-nodes.json")
        else:
            raise ValueError(
                "Unsupported platform.  Only darwin/linux2/win32 are "
                "supported.  You must specify the ipc_path"
            )   
        return node_path

    def get_default_ipc_path(self):

        ''' Return the path of shift IPC file depending on OS '''

        if sys.platform == 'darwin':
            ipc_path = os.path.expanduser("~/Library/gshift/gshift.ipc")
        elif sys.platform == 'linux2':
            ipc_path = os.path.expanduser("~/.gshift/gshift.ipc")
        elif sys.platform == 'win32':
            ipc_path = r"\\.\pipe\gshift.ipc"
        else:
            raise ValueError(
                "Unsupported platform.  Only darwin/linux2/win32 are "
                "supported.  You must specify the ipc_path"
            )
        return ipc_path

    def get_shiftdb_path(self):
        
        """ Return the path to the shift sql database """

        if sys.platform == 'darwin':
            shiftdb = os.path.expanduser("~/Library/gshift/shift.db")
        elif sys.platform == 'linux2':
            shiftdb = os.path.expanduser("~/.gshift/shift.db")
        elif sys.platform == 'win32':
            shiftdb = os.path.expanduser("~\AppData\Roaming\gshift\shift.db")
        else:
            raise ValueError(
                "Unsupported platform.  Only darwin/linux2/win32 are "
                "supported.  You must specify the ipc_path"
            )
        return shiftdb
   
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

        if sys.platform == 'win32':
            res = self.ipc_socket_windows(request)
            return res
            
        elif sys.platform == 'darwin' or sys.platform == 'linux2':
            res = self.ipc_socket(request)
            return res

    def ipc_socket_windows(self, request):

        from Phantom import Error_Msg

        GENERIC_READ = 0x80000000
        GENERIC_WRITE = 0x40000000
        OPEN_EXISTING = 0x3
        INVALID_HANDLE_VALUE = -1
        PIPE_READMODE_MESSAGE = 0x2
        ERROR_PIPE_BUSY = 231
        ERROR_MORE_DATA = 234
        BUFSIZE = 1024

        while True:
            hPipe = windll.kernel32.CreateFileA(self.ipc_path, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, None)
            if (hPipe != INVALID_HANDLE_VALUE):
                break
            else:
                return Error_Msg.error_response("ipc_inv_handle")

            if (windll.kernel32.GetLastError() != ERROR_PIPE_BUSY):
                return Error_Msg.error_response("ipc_err_open")

            elif ((windll.kernel32.WaitNamedPipeA(self.ipc_path, 20000)) == 0):
                return Error_Msg.error_response("ipc_err_open")

        cbWritten = c_ulong(0)
        fSuccess = windll.kernel32.WriteFile(hPipe, c_char_p(request), len(request), byref(cbWritten), None)

        if fSuccess == 0 or (len(request) != cbWritten.value):
            return Error_Msg.error_response("ipc_err_write")

        chBuf = create_string_buffer(BUFSIZE)
        cbRead = c_ulong(0)

        while True:
            fSuccess = windll.kernel32.ReadFile(hPipe, chBuf, BUFSIZE, byref(cbRead), None)
            if fSuccess == 1:
                """ Successfully wrote and read data from named pipe """
                return json.loads(chBuf.value)

            elif (windll.kernel32.GetLastError() == ERROR_MORE_DATA):
                return Error_Msg.error_response("ipc_buff_overflow")

        windll.kernel32.CloseHandle(hPipe)
        return Error_Msg.error_response("ipc_err_write")

    def ipc_socket(self, request):

        for _ in range(3):
            try:
                self._socket.sendall(request)
                response_raw = ""
            except Exception as e:
                pass

            while True:
                try:
                    print response_raw
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

        self.response = json.loads(response_raw)

        if "error" in self.response:
            raise ValueError(self.response["error"]["message"])

        return self.response
