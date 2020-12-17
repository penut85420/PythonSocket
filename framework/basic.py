import os
import json
import socket

import nacl.public
import nacl.utils

from .utils import *


class Socket:
    def __init__(self):
        self.conn = None
        self.sk = nacl.public.PrivateKey.generate()
        self.pk = self.sk.public_key
        # Public key from the other side
        self.the_pk = None

    def _recv(self, size=1024):
        # Receive a message without encrypting, only use for change public key
        data = self.conn.recv(size)
        if os.getenv('VERBOSE'): print(data)
        data = data.decode('UTF-8')
        return json.loads(data)

    def _send(self, **kwargs):
        # Send a message without encrypting, only use for exchange public key
        msg = json.dumps(kwargs)
        self.conn.sendall(msg.encode('UTF-8'))

    def recv(self, size=1024):
        # Receive a message and decrypt it, also get new public from sender
        data = self.conn.recv(size)
        if os.getenv('VERBOSE'): print(data)
        box = nacl.public.Box(self.sk, self.the_pk)
        msg = box.decrypt(data).decode('UTF-8')
        msg = json.loads(msg)
        self.the_pk = hex_to_public_key(msg['__key__'])

        return msg.get('msg', ''), msg

    def send(self, **kwargs):
        # Generate new keys
        new_sk = nacl.public.PrivateKey.generate()
        self.pk = new_sk.public_key

        # Add key into message body
        kwargs['__key__'] = bytes_to_hex(self.pk)
        msg = json.dumps(kwargs).encode('UTF-8')

        # Encrypt message
        box = nacl.public.Box(self.sk, self.the_pk)
        nonce = nacl.utils.random(nacl.public.Box.NONCE_SIZE)
        msg = box.encrypt(msg, nonce)
        self.conn.sendall(msg)

        # Change key
        self.sk = new_sk

class Server(Socket):
    def __init__(self, host='', port=50007):
        # Initialize socket
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.addr = None
        print('Ready!')

        # Listen
        self.socket.listen(1)
        self.conn, (addr, port) = self.socket.accept()
        print(f'Connected by {addr}:{port}')

        # Receive client public key
        msg = self._recv()
        self.the_pk = hex_to_public_key(msg['key'])

        # Send server public key
        self._send(key=bytes_to_hex(self.pk))

class Client(Socket):
    def __init__(self, host='localhost', port=50007):
        # Initialize connection
        super().__init__()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))

        # Send client public key
        self._send(key=bytes_to_hex(self.pk))

        # Receive server public key
        msg = self._recv()
        self.the_pk = hex_to_public_key(msg['key'])
