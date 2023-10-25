# Distributed_cryptoForce

To launch, install the requirements and run `python3 ./main.py`

To launch calculating engine compile ecalc_md5.c

`gcc -shared -I /usr/bin/ssl ecalc_md5.c -Wl,-soname,adder -o ecalc_md5.so -Wl,-rpath /usr/bin/lib -Wl,-L,/usr/bin/lib -lssl -lcrypto`
