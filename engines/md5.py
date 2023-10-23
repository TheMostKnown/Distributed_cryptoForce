import hashlib
from itertools import product
import asyncio
import concurrent.futures as cf
from functools import wraps
import socket

sock = socket.socket()



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
    return "-"

@threadpool
def some_long_calculation(n, my_hash):
	return md5(n, my_hash)



def main()
	sock.bind(('', 9090))
	sock.listen(1)
	conn, addr = sock.accept()
	number = int(0)#28 
	my_hash = str("no")
	while True:
	    data = conn.recv(1024)
	    if not data:
	        break
	    data_all += data
    # extract data
    number, my_hash = data
    result = some_long_calculation(4,"30f64f3171b1fa24a1698bdf0b435b19")
    conn.send(result.result())
    conn.close()

while true:
	main()
