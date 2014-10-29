import socket
import os
from threading import Thread
import time

HOST = ''
PORT = 8080
length = 2**20
random = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

def humanreadable(num, speed=False):
    def output(n, u): return '{:.2f} {}'.format(n, u)
    division = 1000 if speed else 1024
    for unit in ['','k','M','G','T']:
        if num < division:
            return output(num, unit)
        num /= division
    return output(num, unit)

def random_data(length, random):
    if not random:
        return b'\x00'*length
    else:
        return os.urandom(length)

def send_shit(connection, address):
    connection.settimeout(5)
    size = 0
    starttime = time.time()
    while True:
        try:
            connection.sendall(random_data(length, random))
            size += length
        except Exception as e:
            print(e)
            return print(address, 'closed. speed: {}bit/s, size: {}B'.format(
                humanreadable(size * 8 / (time.time() - starttime), speed=True),
                humanreadable(size)
                ))

if __name__ == '__main__':
    http_response = b'HTTP/1.0 200 OK\ncontent-type: application/octet-stream\n\n\n'
    while True:
        conn, addr = s.accept()
        conn.recv(1024)
        print(addr)
        conn.settimeout(5)
        conn.send(http_response)
        Thread(target=send_shit, args=(conn, addr)).start()
