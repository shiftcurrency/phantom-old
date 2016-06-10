from subprocess import Popen, PIPE
from sys import platform

def start():
    try:
        if platform == 'win32':
            command = ['gshift.exe', '--shh', '--rpccorsdomain="*"']
        else:
            command = ['gshift', '--shh', '--rpccorsdomain="*"']

        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=False)
        print "- Started gshift."
        return process
    except Exception as e:
        return False
