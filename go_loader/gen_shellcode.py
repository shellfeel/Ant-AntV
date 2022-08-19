from common.crypto_utils import crypto_utils
from common.project_path import project_path


def test():
    shellcode = crypto_utils.shellcode_decrypt()
    go_str = "shellcode_buf = []byte{"
    for x in shellcode:
        # print(hex(x))
        go_str += hex(x) + ","
    # print(shellcode
    go_str += "}"
    with open(project_path.get_resource_path() + "go_shellcode.bin", "w") as f:
        f.write(go_str)

    print(go_str)


if __name__ == '__main__':
    test()