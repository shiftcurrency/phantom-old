from os import devnull
from os.path import abspath
from subprocess import Popen
from subprocess import check_output
from sys import platform
from Debug import Debug
import logging
import atexit

class Run_Gshift:

    def __init__(self):
        self.log = logging.getLogger("gshift")
        self.process = None
        self.fnull = open(devnull, 'wb')
        self.pidlist = []

    def start(self):
        self.log.info("Starting gshift...")
        try:
            if platform == 'win32':
                command = ['gshift.exe', '--shh']
                self.process = Popen(command, stdout=self.fnull, stderr=self.fnull, shell=False)
            else:
                command = [abspath('gshift'), '--shh']
                self.process = Popen(command, stdout=self.fnull, stderr=self.fnull, shell=True)

            atexit.register(self.stop)
            return self.process

        except Exception, err:
            print "Error starting gshift: %s" % Debug.formatException(err)
            self.log.error("Error starting gshift: %s" % Debug.formatException(err))
            return False


    def check_running_proc(self,name):
        
        import time

        for i in range(1,10):
            try:
                if platform == 'win32':
                   self.pidlist = list(check_output(["tasklist"]).split('\n'))
                   for i in self.pidlist:
                       if "gshift.exe" in i:
                           self.proclist = [x for x in i.split(" ") if x != '']
                           if len(self.proclist) >= 1: return [self.proclist[1]]
                else: 
                    self.pidlist = map(int, check_output(["pidof", name]).split())
                    if len(self.pidlist) > 0: return self.pidlist

            except Exception as e:
                return False

            if i == 10: break
            time.sleep(1)

        return False


    def verify_ipc_connection(self):

        import os
        from Shift_IPC import IPC_Client
        self.check_file = IPC_Client.Client()
        self.check_ipc = IPC_Client.Client()

        for i in range(1,10):
            try:
                self.ipc_connection = self.check_ipc.net_listening()
                if 'result' in self.ipc_connection:
                    return True
            except Exception as e:
                 return False

            if i == 10: break
            time.sleep(1)
        return False


    def stop(self):
        self.log.info("Stopping gshift...")
        try:
            self.process.terminate()
        except Exception, err:
            self.log.error("Error stopping gshift: %s" % err)
