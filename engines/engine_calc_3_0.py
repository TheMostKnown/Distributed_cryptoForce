import socket
import json
import multiprocessing
import threading
import time
from ctypes import *

md5 = CDLL('./ecalc_md5.so')

#host = socket.gethostname() # as both code is running on same pc
host = '10.1.1.43'
#port = 5001  # socket server port number
SOURCE_PORT, DESTINATION_PORT = 6666, 9090
#characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
kill_phrase = 'Interrupt'

def return_proc_res(queue, func, num, req_hash):
    #print("Process of Python get res md5 - ", multiprocessing.current_process())
    try:
        print("The calculations have begun.")
        r = func(c_int(num), c_char_p(str.encode(req_hash)))
        queue.put(r)
        print("The calculations ended. Result - ", r.decode('utf-8'))
    except Exception as e:
        print("proc_res error")
        queue.put(0)
    finally:
        pass
    


def listen_socket_state(queue, some_socket):
    try:
        print("Process of listening socket started ")
        r = some_socket.recv(1024)
        while not queue.empty():
            time.sleep(0.1)
        queue.put(r)
        print("Process of listening socket ended. Received - ", r.decode('utf-8'))
    except Exception as e:
        #print("Process of Python socket state error", e)
        pass


def client_program(queue_flag):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    flag = True
    number = 0
    req_hash = ""

    try:
        #client_socket.bind(('0.0.0.0', SOURCE_PORT))
        client_socket.connect((host, DESTINATION_PORT))  # connect to the server
        data = client_socket.recv(1024)
        parameters = json.loads(data)  # receive response
        number = int(parameters['number'])
        req_hash = parameters['hash']
        print("Connection established. number - ", number, " hash - ", req_hash)

    except Exception as e:
        client_socket.close()
        time.sleep(0.5)
        print(e, "connect")
        queue_flag.put(0)
        return

    

    while flag:
        queue = multiprocessing.Queue()
        ########################################################
        brute_md5 = md5.return_md5
        brute_md5.restype = c_char_p
        brute_md5.argtypes = [c_int, c_char_p]
        proc = multiprocessing.Process(target=return_proc_res, args=(queue, brute_md5, number, req_hash))
        proc.start()
        listen_SIGKILL_thread = threading.Thread(target=listen_socket_state, args=(queue, client_socket))
        listen_SIGKILL_thread.start()
        ########################################################

        res = queue.get().decode('utf-8')
        #or kill phrase or answer
        #print(res, ' ', res == kill_phrase)
        if (res != "None") or (res == kill_phrase):
            if res == kill_phrase:
                proc.terminate()
                queue_flag.put(0)
                client_socket.close()
                return
            flag = not flag

        try:
            client_socket.send(res.encode())
            print("The answer is sended to the manager.")
        except Exception as e:
            break
        #client_socket.send(res)
        proc.terminate()
        #print("Process of Python client program - ", multiprocessing.current_process())
        #print(f"{flag}")
        if flag:
            # if queue.empty():
            #print("Q: ")
            msg = queue.get()
            #wait dor number data or interrupt signal
            #print("Q: ",msg)
            if msg != kill_phrase:
                number = int(msg)
                #flag = not flag
            else:
                queue_flag.put(0)
                client_socket.close()
                return

    client_socket.close()
    print("Connection closed.")
    queue_flag.put(0)
    return

if __name__ == '__main__':
    while True:
        #print("Process of Python main md5 - ", multiprocessing.current_process())
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=client_program, args=(queue,))
        p.start()
        if queue.get() == 0:
            p.terminate()
            continue