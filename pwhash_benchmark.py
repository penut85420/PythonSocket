import nacl.pwhash
import datetime as dt

class TimeCost:
    def __init__(self, msg='Time Cost', verbose=True):
        self.ts = None
        self.verbose = verbose
        self.msg = msg

    def __enter__(self):
        self.ts = dt.datetime.now()

    def __exit__(self, *args):
        self.ts = dt.datetime.now() - self.ts
        if self.verbose:
            print(f'{self.msg}: {self.ts.total_seconds()}s')

def main():
    password = b'my password'

    methods = [
        nacl.pwhash,
        nacl.pwhash.scrypt,
        nacl.pwhash.argon2i,
        nacl.pwhash.argon2id
    ]
    names = ['pwhash', 'scrypt', 'argon2i', 'argon2id']
    total = 100
    for method, name in zip(methods, names):
        with TimeCost(f'{name:8s}'):
            for i in range(total):
                print(f'{i+1}/{total}', end='\r')
                h = getattr(method, 'str')(password)
                res = getattr(method, 'verify')(h, password)

if __name__ == "__main__":
    main()

"""
=== Results ===
pwhash  : 9.894969s
scrypt  : 4.242719s
argon2i : 8.762217s
argon2id: 9.939594s
"""
