from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad


def send_encrypted(secret_key, channel, message):
    '''
    Encrypt the message after creating a cipher,
    and send it over the channel passed as parameter.
    '''
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(message, AES.block_size))
    channel.send(iv + encrypted)