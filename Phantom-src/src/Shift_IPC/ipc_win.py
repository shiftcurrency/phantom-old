from ctypes import *


GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 0x3
INVALID_HANDLE_VALUE = -1
PIPE_READMODE_MESSAGE = 0x2
ERROR_PIPE_BUSY = 231
ERROR_MORE_DATA = 234
BUFSIZE = 512


#MESSAGE = '{"jsonrpc":"2.0","method":"net_listening","params":[],"id":1}'

MESSAGE = '{"jsonrpc":"2.0","method":"shf_getBalance","params":["0x2e201bf5a75ba5d58af0ae919ab580995cf63f9b", "latest"],"id":1}' 

#MESSAGE = '{"jsonrpc":"2.0","method":"shf_blockNumber","params":[],"id":1}' 

name = 'gshift.ipc'
szPipename = r"\\.\pipe\%s" % name

def Pipe_Client():

    while 1:
        hPipe = windll.kernel32.CreateFileA(szPipename, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, None)
        if (hPipe != INVALID_HANDLE_VALUE):
             break
        else:
            print "Invalid Handle Value"

        if (windll.kernel32.GetLastError() != ERROR_PIPE_BUSY):
            print "Could not open pipe"
            return

        elif ((windll.kernel32.WaitNamedPipeA(szPipename, 20000)) == 0):
            print "Could not open pipe\n"
            return

    dwMode = c_ulong(PIPE_READMODE_MESSAGE)
    fSuccess = windll.kernel32.SetNamedPipeHandleState(hPipe, byref(dwMode), None, None);

    if (not fSuccess):
        print "SetNamedPipeHandleState failed"

    cbWritten = c_ulong(0)
    fSuccess = windll.kernel32.WriteFile(hPipe, c_char_p(MESSAGE), len(MESSAGE), byref(cbWritten), None)

    if ((not fSuccess) or (len(MESSAGE) != cbWritten.value)):
        print "Write File failed"
        return

    else:
        print "Number of bytes written:", cbWritten.value

    fSuccess = 0
    chBuf = create_string_buffer(BUFSIZE)
    cbRead = c_ulong(0)

    while (not fSuccess): # repeat loop if ERROR_MORE_DATA
        fSuccess = windll.kernel32.ReadFile(hPipe, chBuf, BUFSIZE, byref(cbRead), None)
        if (fSuccess == 1):
            print "Number of bytes read:", cbRead.value
            print chBuf.value
            break

        elif (windll.kernel32.GetLastError() != ERROR_MORE_DATA):
            break

    windll.kernel32.CloseHandle(hPipe)
    return

if __name__ == "__main__":
    Pipe_Client()


