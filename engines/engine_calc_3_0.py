import socket
import json
import select
import multiprocessing
import threading
import time
from ctypes import *

md5 = CDLL('./ecalc_md5.so')

host = socket.gethostname() # as both code is running on same pc
#port = 5001  # socket server port number
SOURCE_PORT, DESTINATION_PORT = 6666, 5001
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
kill_phrase = 'SIGKILL'

def return_proc_res(queue, func, num, req_hash):
    queue.put(func(c_int(num), c_char_p(str.encode(req_hash))))


def listen_socket_state(queue, some_socket):
    try:
        queue.put(some_socket.recv(1024).decode('utf-8'))
    except Exception as e:
        pass


def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    flag = True
    number = 0
    req_hash = ""
    try:
        sock.bind(('0.0.0.0', SOURCE_PORT))
        client_socket.connect((host, DESTINATION_PORT))  # connect to the server
        data = client_socket.recv(1024)
        parameters = json.loads(data)  # receive response
        number = int(parameters['number'])
        req_hash = parameters['hash']

    except Exception as e:
        client_socket.close()
        time.sleep(0.5)
        return

    while flag:

        ########################################################
        brute_md5 = md5.return_md5
        brute_md5.restype = c_char_p
        brute_md5.argtypes = [c_int, c_char_p]
        queue = multiprocessing.Queue()
        proc = multiprocessing.Process(target=return_proc_res, args=(queue, brute_md5, number, req_hash))
        proc.start()
        listen_SIGKILL_thread = threading.Thread(target=listen_socket_state, args=(queue, client_socket))
        listen_SIGKILL_thread.start()
        ########################################################

        res = queue.get()
        if res != 'None' or res == kill_phrase:
            if res == kill_phrase:
                proc.terminate()
                return
            flag = not flag

        try:
            client_socket.send(res)
        except Exception as e:
            break
        #client_socket.send(res)
        if flag:
            msg = queue.get()
            if msg != kill_phrase:
                number = int()
            else:
                return
    client_socket.close()
    return

if __name__ == '__main__':
    while True:
        client_program()