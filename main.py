import argparse
from framework import Server, Client

class MyServer(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Begin turn-based conversation
        msg = ''
        while 'Bye!' not in msg:
            msg, _ = self.recv()
            print(msg)
            if 'Bye!' in msg:
                break
            msg = input(" > ").strip()
            self.send(msg=f'Server: {msg}')

        print('\nConversation done!')

class MyClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        MyServer(args.host, args.port)
    elif args.client:
        MyClient(args.host, args.port)
