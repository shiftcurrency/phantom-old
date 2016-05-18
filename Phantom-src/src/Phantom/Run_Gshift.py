from subprocess import Popen, PIPE

def start():
    try:
        process = Popen(['gshift', '--shh'], stdout=PIPE, stderr=PIPE, shell=False)
        print "- Started gshift."
        return process
    except Exception as e:
        return False
