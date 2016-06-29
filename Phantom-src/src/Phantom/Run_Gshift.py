from subprocess import Popen, PIPE
from sys import platform
from Debug import Debug
import logging
import atexit

class Run_Gshift:

    def __init__(self):
        self.log = logging.getLogger("gshift")
        self.process = None

    def start(self):
        self.log.info("Starting gshift...")
        try:
            if platform == 'win':
                command = ['gshift.exe', '--shh']
                self.process = Popen(command, stdout=PIPE, stderr=PIPE, shell=False)
            else:
                command = ['gshift', '--shh']
                self.process = Popen(command, stdout=PIPE, stderr=PIPE, shell=False)

                # Terminate on exit
                atexit.register(self.stop)
            return self.process

        except Exception, err:
            print "Error starting gshift: %s" % Debug.formatException(err)
            self.log.error("Error starting gshift: %s" % Debug.formatException(err))
            return False

    def stop(self):
        self.log.info("Stopping gshift...")
        try:
            self.process.terminate()
        except Exception, err:
            self.log.error("Error stopping gshift: %s" % err)
