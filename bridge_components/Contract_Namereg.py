#!/usr/bin/env python
import json
import requests
import sys
from eth_abi.abi import encode_single
#from Config import config

def rpc_call(method, params):

    ''' Template for RPC calls against phantom binary '''
    data = "{\"jsonrpc\":\"2.0\", \"method\":\"%s\", \"params\":%s, \"id\": \"1\"}" % (method,params)
    print data

    response = requests.post("http://localhost:53901", data=data)
    jsondata = response.json()
    
    if 'result' in jsondata:
        return jsondata['result']
    return jsondata['error']



def get_shiftbase():

    res = shiftrpc("shf_shiftbase", [], "")

    if res and 'result' in res and len(res['result']) == 42:
        return res['result']

    return False



def get_zeroshifthash(domain):

    method = 'shf_call'
    prepend = "0xf39ec1f7"

    domain_hex = domain.encode("hex")
    print domain_hex

    while len(domain_hex) != 66:
        domain_hex = domain_hex + "0"

    ''' The final concatenated call '''
   
    params = "[{\"to\": \"0xef7740b6a763cc1886f6764eb568b549402a3170\", \"data\": \"%s\" }]" % call_data
    res = rpc_call(method, params)

    print res
    if not res:
        return False

    ''' This shall always be 68 chars long, so we can hard code this. '''



def register_domain(domain, zerohash):

    ''' Example string of RPC call
    "0xa87956e663726565642e636f6d000000000000000000000000000000000000000000000031365379697038765970514c6b57467a344e77354c4470326254456259436850000000000000000000000000000000000000000000000000000000000a594c"
    '''

    ''' Use shf_call for calling a contract at a specific address. '''
    method = 'shf_sendTransaction'
    prepend = "0x"
    
    ''' Prepending the first 4 bytes of sha3 hash of the function. '''
    domain_hex = domain.encode("hex")
    domain_hex_pad = "0"

    ''' Pad the hex encoded domain string with zeros of 64 chars. '''
    while len(domain_hex_pad) != 48:
        domain_hex_pad = domain_hex_pad + "0"

    domain_hex = domain_hex_pad + domain_hex

    ''' The zerohash should always be 34 chars long, else something is wrong. '''
    if len(zerohash) != 34: return False

    ''' We need to split the zerohash into several parts to fit in the byte32 array. '''
    zerohash_hex = zerohash.encode("hex")
    zerohash_first32 = zerohash_hex[:-5]
    zerohash_last32 = zerohash_hex[-5:]

    ''' Pre pad the last four chars with zeros. '''
    last32_padding = ""

    while len(last32_padding) != 58:
        last32_padding = last32_padding + "0"

    call_data = prepend + domain_hex + zerohash_first32 + last32_padding + zerohash_last32

    ''' In version 0.0.1a the call data should be 200 chars long. '''
    if len(call_data) != 200: return False

    params = "[{\"from\": \"0x6fa5cbef987a9b32dee3a6d6a72abf3ebf79e8ea\", \"to\": \"0x0e81ae3d13576bc0c81c27d1f4cff0840419450f\", \"gas\": \"300000\", \"data\": \"%s\" }]" % call_data
    transaction_hash = rpc_call(method, params)

    if not transaction_hash: return False

    
    return transaction_hash



def test_rpc_conn():

    res = get_shiftbase()

    if not res:
        return False
    return True



if __name__ == "__main__":

    res = get_zeroshifthash("wallet.shift")
    print res
