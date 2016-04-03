import os
import shutil
import sys
import json
import subprocess
import threading
import re
import requests
import time


constants(call, domain_name):

    ''' Using this method instead a config.ini and ConfigParser due to compability and py2exe size '''

    if call == "domain_available":
        return "[%d Phantom Bridge ] - Domain is available, trying to register on Phantom..." % (int(time.time()))

    elif call == "register_success":
        return "[%d Phantom Bridge ] - You have successfully registered and indexed your Phantom site: %s" % (int(time.time()), domain_name)

    elif call == "insufficient_balance"
        return "[%d Phantom Bridge ] - You do not have enough balance to pay the fee for registering a Phantom site." % (int(time.time())

    elif call == "domain_notavail":
        return "[%d Phantom Bridge ] - The domain you tried to register is already registered, try another or just use a random string." % (int(time.time()))

    elif call == "domain_notvalid":
        return "[%d Phantom Bridge ] - Not a valid domain name. The domain name must end with .gn, e.g. domain.gn" % (int(time.time()))

    elif call == "exiting":
        return "\n\n[%d Phantom Bridge ] - Exiting." % (int(time.time()))

    elif call == "wrote_domain":
        return "[%d Phantom Bridge ] - Wrote domain: %s into names.json." % (int(time.time()), domain_name)

    elif call == "no_website":
        return "[%d Phantom Bridge ] - Could not create default website for address %s. Create your own." % (int(time.time()), address)

    elif call == "success":
        return "[%d Phantom Bridge ] - Created default website for address %s." % (int(time.time()), address)
    else:
        return 0




def shiftRPC(self, method, params):

    data = json.dumps({"jsonrpc":"2.0", "method":method, "params":[], "id":1})
    response = requests.post("http://localhost:51501", data=data)
    jsondata = response.json()
    
    if 'result' in jsondata:
        return jsondata['result']
    return jsondata['error']



def ask_user(self, zeroshift_hash, shift_conf):

    while True:
        try:    
            domain_name = raw_input('-- Enter a domain name that can be used to reach your Phantom site: ')
            if domain_name.endswith(".gn"):

                if self.domain_free(domain_name, shift_conf):
                    print constants("domain_available")

                    if self.enough_balance(self.get_fee(), shift_conf):

                        if self.domain_new(domain_name, zeroshift_hash):
                            print constants("success", domain_name)
                            return domain_name
                    else:
                        print constants("insufficient_balance", domain_name)
                        sys.exit(0)
                else:
                    print constants("domain_notavail", domain_name)
                    continue
            else:
                print constants("domain_notvalid", domain_name)
                continue
        except KeyboardInterrupt:
            print constants("exiting", domain_name)
            sys.exit(0)


def get_fee(self):

    ## Do not change this. If you do you will not be able to do the transaction since
    ## this fee is hardcoded into shift cryptocurrency network.
    return 10000


def enough_balance(self, fee, shift_conf):

    balances = json.loads(self.rpc_template('listaccounts', [], shift_conf))
    if balances.has_key('result') and len(balances['result']) > 0:
        for account_balance in balances['result']:
            balance= balances['result'][account_balance]
            if balance > fee:
                return True
    return False


def list_unspent(self, fee, shift_conf):

    accounts = json.loads(self.rpc_template('listunspent', [], shift_conf))
    if accounts.has_key('result'):
        for account in accounts['result']:
            if account['address'] == public_key and account['txid'] != "" and \
                account['vout'] != "":
                return account
    return False


def domain_free(self, dm, shift_conf):
    
    domains = json.loads(self.rpc_template('name_list', [], shift_conf))
    if domains.has_key('result'):
        for domain in domains['result']:
            if domain['name'] == dm:
                return False ## Domain exists or in a pending state
        return True ## Domain is free to register
    return None


def domain_new(self, dm, shiftaddr):
    return 0


def site_sign(self, shift_addr, shift_conf):

    if shift_addr and shift_conf:
        domain_name = raw_input('Enter the domain name of the site you want to sign: ')
        domains = json.loads(self.rpc_template('name_list', [], shift_conf))
        if domains.has_key('result'):
            for domain in domains['result']:
                if domain['name'] == domain_name and domain['value'] == shift_addr and \
                self.update_single_domain(domain_name, shift_addr):
                    return { 'retcode' : True, 'val' : domain['name'] }
        return { 'retcode' : False, 'val' : "The domain must be indexed on blockchain before signing. Exiting." }
    else:
        return { 'retcode' : False, 'val' : "Missing arguments for signing. Exiting." }
    return { 'retcode' : False, 'val' : " The domain name does not match Phantom address. Exiting." }



def update_single_domain(self, dm, address):

    if dm and address:
        name_json = { dm : address }
        dir_path = os.path.abspath(".")
        dir_path = dir_path + '/data/' + address + "/data/"

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        file_path = dir_path + 'names.json'

        with open(file_path, 'w') as fp:
            if not json.dump(name_json, fp):
                print "[%d Phantom Bridge ] - Wrote domain: %s into names.json." % (int(time.time()), dm)
                return True


def update_domains(self, address):


    dir_path = os.path.abspath(".")
    dir_path = dir_path + '/data/' + address + "/data/"
    if not os.path.isdir(dir_path):
        os.makedirs(dirpath)

    file_path = dir_path + 'names.json'
    print file_path
    names = json.loads(self.rpc_template('name_scan', [], self.get_conf()))
    # Be sure that we have something to parse

    names_jsonformatted = {}
    if names.has_key('result') and len(names['result']) > 0:
    # names are a dict, variable "i" contains a list of other dicts
        for i in (names['result']):
        # Generate a new dict that will fit names.json format.
            names_jsonformatted[i['name']] = i['value']


    with open(file_path, 'w') as fp: 
            if not json.dump(names_jsonformatted, fp):
                print "[%d Phantom Bridge ] - Wrote new domains from Phantom network into names.json." % (int(time.time()))



def create_defaultsite(self, address):

    import shutil
    dir_path = os.path.abspath(".")
    to_dir = dir_path + '/data/' + address + '/' 
    from_dir = dir_path + '/src/Bridge/default_website/'

    for item in os.listdir(from_dir):
        s = os.path.join(from_dir, item)
        d = os.path.join(to_dir, item)
        if os.path.isdir(s):
            try:
                shutil.copytree(s, d, symlinks=False, ignore=None)
            except Exception as e:
                if 'Errno 17' in str(e):
                    pass
                else:
                    print "[%d Phantom Bridge ] - Could not create default website for address %s. Create your own." % (int(time.time()), address)
                    return False
        else:
            try:
                shutil.copy2(s, d)
            except Exception as e:
                print "[%d Phantom Bridge ] - Could not create default website for address %s. Create your own." % (int(time.time()), address)
                print e
                return False

        print "[%d Phantom Bridge ] - Created default website for address %s." % (int(time.time()), address)
        return True


def check_rpc_status(self):
    


if __name__ == "__main__":
    check_rpc_status
