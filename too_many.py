import threading
import string
import random
import argparse
from framework import Server, Client

class RootServer(Server):
    def __init__(self, *args, **kwargs):
        self.ports = list(range(40000, 50000))
        super().__init__(*args, **kwargs)

        while True:
            port = self.ports[0]
            print(f'Send port {port}')
            threading.Thread(target=Chatbot, args=(self, self.host, port)).start()
            self.send(port=self.ports[0])
            self.ports = self.ports[1:]
            try:
                self.listen()
            except KeyboardInterrupt:
                print('\n\nBye!')
                exit(0)
            self.exchange()

class Chatbot(Server):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Begin turn-based conversation
        msg = ''
        while 'Bye!' not in msg:
            msg, _ = self.recv()
            print(f'[{self.port}] {msg}')
            if 'Bye!' in msg:
                break
            msg = ''.join([random.choice(string.ascii_letters) for _ in range(random.randint(5, 10))])
            self.send(msg=f'Server: {msg}')

        print(f'[{self.port}] Conversation done!')
        root.ports.append(self.port)

class MyClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect(self.host, self.port)

        _, msg = self.recv()
        print(f'Get port {msg["port"]}')
        self.connect(host=self.host, port=msg['port'])

        # Begin turn-based conversation
        msg = ''
        while 'Bye!' not in msg:
            msg = input(" > ").strip()
            self.send(msg=f'Client: {msg}')
            if 'Bye!' in msg:
                break
            msg, raw = self.recv()
            print(msg)

        print('\nConversation done!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Simple socket conversation with the public key encryption')
    parser.add_argument(
        '--server', action='store_true', default=False, help='Start the program as a server')
    parser.add_argument(
        '--client', action='store_true', default=False, help='Start the program as a client')
    parser.add_argument(
        '--host', default='localhost', type=str, help='Assign the host')
    parser.add_argument(
        '--port', default=50007, type=int, help='Assign the port')
    args = parser.parse_args()

    if args.server:
        RootServer(host=args.host, port=args.port)
    elif args.client:
        MyClient(host=args.host, port=args.port)
