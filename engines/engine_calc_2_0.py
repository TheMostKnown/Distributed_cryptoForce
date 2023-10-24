import socket
import json
import hashlib
from itertools import product
import asyncio
import concurrent.futures as cf
from functools import wraps
import multiprocessing
import threading
import time

host = socket.gethostname() # as both code is running on same pc
port = 5001  # socket server port number
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
kill_phrase = 'SIGKILL'
_DEFAULT_POOL = cf.ThreadPoolExecutor()

def threadpool(f, executor=None):
    @wraps(f)
    def wrap(*args, **kwargs):
        return (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)

    return wrap

def md5(n, my_hash):
    for combos in product(characters, repeat=n):
        S = ''.join(combos)
        result = hashlib.md5(S.encode('ASCII'))
        if result.hexdigest() == my_hash:
            return S
    return 'None'

@threadpool
def some_long_calculation(n, req_hash):
    return md5(n, req_hash)

def return_proc_res(queue, func, num, req_hash):
    queue.put(func(num, req_hash))

def return_socket_state(queue, some_socket):
    queue.put(some_socket.recv(1024).decode('utf-8'))


def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    flag = True
    number = 0
    req_hash = ""
    try:
        client_socket.connect((host, port))  # connect to the server
        data = client_socket.recv(1024)
        parameters = json.loads(data)  # receive response
        number = parameters['number']
        req_hash = parameters['hash']
    except Exception as e:
        #print(f"Ошибка при подключении к серверу: {e}")
        client_socket.close()
        time.sleep(0.2)
        return

    while flag:
        #Вот это бы во второй процесс
        ########################################################
        queue = multiprocessing.Queue()
        proc = multiprocessing.Process(target=return_proc_res, args=(queue, md5, number, req_hash))
        proc.start()
        #result = some_long_calculation(number, req_hash)
        ########################################################
        listen_SIGKILL_thread = threading.Thread(target=return_socket_state, args=(queue, client_socket))
        listen_SIGKILL_thread.start()
        res = queue.get()
        #res = result.result()
        if res != 'None' && res != kill_phrase:
            if res == kill_phrase:
                proc.terminate()
                return
            flag = not flag

        if flag:
            number = int(queue.get())

        client_socket.send(res.encode())

    client_socket.close()
    return

if __name__ == '__main__':
    while True:
        client_program()