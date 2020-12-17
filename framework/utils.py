import io

import nacl.public
import PIL.Image
import pyotp
import qrcode


def hex_to_public_key(hex):
    key = hex_to_bytes(hex)
    return nacl.public.PublicKey(key)

def img_to_bytes(img):
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')

    return img_bytes.getvalue()

def img_from_bytes(img_bytes):
    image = PIL.Image.open(io.BytesIO(img_bytes))

    return image

def bytes_to_hex(b):
    return bytes(b).hex()

def hex_to_bytes(h):
    return bytes(bytearray.fromhex(h))

def generate_otp():
    rnd = pyotp.random_base32()
    totp = pyotp.totp.TOTP(rnd)
    url = totp.provisioning_uri(name='Hello', issuer_name='Oppai')

    return url, totp

def gen_qrcode(msg, fp):
    qrcode.make(msg).save(fp)
