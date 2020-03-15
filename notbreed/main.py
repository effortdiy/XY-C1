import paramiko
from scp import SCPClient

import sys
import os

root_path = os.path.abspath(os.getcwd())


HOST = "192.168.1.1"
PORT = "22"
USERNAME = "root"
PASSWORD = "1234.abcd"
BREED = "breed.bin"


def uploadFile2Remote():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(HOST, PORT, USERNAME, PASSWORD)
    scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)
    try:
        scpclient.put(os.path.join(root_path, BREED), '/tmp/breed.bin')
    except FileNotFoundError as e:
        print(e)
        print("系统找不到指定文件" + BREED)
    else:
        print("文件上传成功")
    ssh_client.close()


def execShell():
    # 创建一个ssh的客户端，用来连接服务器
    ssh = paramiko.SSHClient()
    # 创建一个ssh的白名单
    know_host = paramiko.AutoAddPolicy()
    # 加载创建的白名单
    ssh.set_missing_host_key_policy(know_host)

    # 连接服务器
    ssh.connect(
        hostname=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD
    )

    stdin, stdout, stderr = ssh.exec_command("mtd write /tmp/breed.bin u-boot")

    print(stdout.read().decode())
    stdin, stdout, stderr = ssh.exec_command("cat /proc/mtd")

    print(stdout.read().decode())
    ssh.close()


if __name__ == "__main__":
    print("默认ip：192.168.1.1")
    print("默认账号：root")
    print("默认密码：1234.abcd")
    print("默认breed.bin地址为当前目录下breed.bin：")
    print("回车直接默认！")
    try:
        uploadFile2Remote()
        execShell()
    except Exception as e:
        print(e)
    print("完成,任意键退出!")
