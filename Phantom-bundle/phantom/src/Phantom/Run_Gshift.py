from subprocess import Popen, PIPE
import os
import signal


def start():
    try:
        process = Popen(['gshift', '--shh'], stdout=PIPE, stderr=PIPE, shell=False)
        print "- Started gshift."
        return process
    except Exception as e:
        print e
