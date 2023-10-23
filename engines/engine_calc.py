import socket
import json
import hashlib
from itertools import product
import asyncio
import concurrent.futures as cf
from functools import wraps

host = socket.gethostname() # as both code is running on same pc
port = 5001  # socket server port number
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

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
def some_long_calculation(n, my_hash):
    return md5(n, my_hash)

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    flag = True
    number = 0
    rec_hash = ""
    try:
        client_socket.connect((host, port))  # connect to the server
        data = client_socket.recv(1024)
        parameters = json.loads(data)  # receive response
        number = parameters['number']
        rec_hash = parameters['hash']
    except Exception as e:
        #print(f"Ошибка при подключении к серверу: {e}")
        return

    while flag:
        #Вот это бы во второй процесс
        ########################################################
        result = some_long_calculation(number, rec_hash)
        ########################################################
        res = result.result()
        if res != 'None':
            flag = not flag

        client_socket.send(res.encode())

        if flag:
            number = int(client_socket.recv(1024).decode('utf-8'))
    return
            
    client_socket.close()
if __name__ == '__main__':
    while True:
        client_program()