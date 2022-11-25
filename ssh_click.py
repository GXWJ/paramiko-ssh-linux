import os.path
from tkinter import *
import paramiko
import tkinter

# 创建一个GUI窗口
window = tkinter.Tk()
window.title('ssh连接')
window.geometry('968x640')  # 设置窗口大小:宽x高,注,此处不能为 "*",必须使用 "x"
# 创建ssh连接输入框
entry_host = tkinter.Entry(window)  # 创建输入框控件
entry_host.place(relx=0.01, rely=0.01, relheight=0.04, relwidth=0.15)  # hostname
entry_host.insert(INSERT, "127.0.0.1")
entry_user = tkinter.Entry(window)  # 创建输入框控件
entry_user.place(relx=0.17, rely=0.01, relheight=0.04, relwidth=0.15)  # user
entry_user.insert(INSERT, "root")
entry_paw = tkinter.Entry(window)  # 创建输入框控件
entry_paw.place(relx=0.33, rely=0.01, relheight=0.04, relwidth=0.15)  # password
entry_paw.insert(INSERT, "root")
entry_point = tkinter.Entry(window)  # 创建输入框控件
entry_point.place(relx=0.50, rely=0.01, relheight=0.04, relwidth=0.03)  # point
entry_point.insert(INSERT, '22')


def configuration():
    hostname = entry_host.get()
    point = int(entry_point.get())
    username = entry_user.get()
    password = entry_paw.get()
    return hostname, point, username, password


def ssh_line():
    hostname, point, username, password = configuration()
    print('ssh_line')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect("主机名", 端口22, "用户名", "密码", "超时时间")
    print(f"hostname={hostname}, port={point}, username={username}, password={password}")
    print(f"hostname={type(hostname)}, port={type(point)}, username={type(username)}, password={type(password)}")
    if password == '':
        ssh.connect(hostname=hostname, port=point, username=username, timeout=10,look_for_keys=False)
    else:
        ssh.connect(hostname=hostname, port=point, username=username, password=password, timeout=10, look_for_keys=False)
    return ssh


def ssh_shell(order):
    print("ssh_shell")
    ssh = ssh_line()
    stdin, stdout, stderr = ssh.exec_command(order)
    # 输出返回信息
    stdout_info = stdout.read().decode('utf8')
    # 输出返回的错误信息
    stderr_info = stderr.read().decode('utf8')
    text.insert(END, f'运行指令：{order}\n')
    text.insert(END, stdout_info)
    if stderr_info != '':
        print(stderr_info)
        text.insert(END, stderr_info)
    print(type(stdout_info))
    print(stdout_info)
    return stdout_info


def up_file():
    print('up_file')
    hostname, point, username, password = configuration()
    # 获取Transport实例
    tran = paramiko.Transport(hostname, point)
    # 连接SSH服务端
    tran.connect(username=username, password=password)
    # 获取SFTP实例
    sftp = paramiko.SFTPClient.from_transport(tran)
    # 设置上传的本地/远程文件路径
    localpath = entry2.get()  # 本地文件路径
    remotepath = entry3.get()  # 上传对象保存的文件路径
    # 执行上传动作
    if os.path.isdir(entry2.get()):  # 判断是否为文件夹
        filelist = os.listdir(entry2.get())
        for file in filelist:
            local_path = entry2.get() + '\\' + file
            print(local_path)
            remote_path = entry3.get() + '/' + file
            sftp.put(localpath=local_path, remotepath=remote_path)
        tran.close()
    else:
        sftp.put(localpath=localpath, remotepath=remotepath)
        tran.close()


def download_file():
    print('download_file')
    # 获取Transport实例
    hostname, point, username, password = configuration()
    tran = paramiko.Transport(hostname, point)
    # 连接SSH服务端
    tran.connect(username=username, password=password)
    # 获取SFTP实例
    sftp = paramiko.SFTPClient.from_transport(tran)
    # 截取下载文件名称
    file_name = entry3.get()[entry3.get().rindex('/') + 1:]
    file_path = entry3.get()[:entry3.get().rindex('/')]
    print("..." + file_path)
    # 判断为文件还是文件夹
    file_type = list(ssh_shell(f'ls -l {file_path}|grep {file_name}'))[0]
    print(file_type)
    if file_type == 'd':
        file_path = entry2.get()
        # 创建文件夹
        os.makedirs(file_path, exist_ok=True)
        file_list = ssh_shell(f'ls {entry3.get()}').splitlines()
        for file in file_list:
            local_path = entry2.get() + '\\' + file
            remote_path = entry3.get() + '/' + file
            sftp.get(remote_path, local_path)
        tran.close()
    else:
        # 设置下载的本地/远程文件路径
        localpath = entry2.get()
        remotepath = entry3.get()
        print(localpath)
        print(remotepath)
        sftp.get(remotepath, localpath)
        tran.close()


def text2_default():
    print('text2_default')
    file = open(file="./default.txt", mode='a+', encoding='utf8')
    file.seek(0)
    if os.path.getsize('default.txt') == 0:
        text2.insert(INSERT, "常用指令:\n")
    else:
        file.seek(0)
        file_content = file.read()
        text2.insert(INSERT, file_content)
        file.close()


def ok_file():
    print('ok_file')
    file = open(file="./default.txt", mode='w', encoding='utf8')
    text_content = text2.get(1.0, END)
    file.write(text_content)
    file.close()


def delete():
    print('delete')
    text.delete(1.0, END)


def run_shell():
    print('run_shell')
    ssh_shell(entry1.get())
    text.insert(END, "\n")


def broken_linke():
    print('broken_linke')
    ssh_line().close()


but_link = tkinter.Button(window, text="连接", command=ssh_line).place(relx=0.54, rely=0.01, relheight=0.04,
                                                                       relwidth=0.1)
but_broken = tkinter.Button(window, text="断开连接", command=broken_linke).place(relx=0.65, rely=0.01, relheight=0.04,
                                                                                 relwidth=0.1)
entry1 = tkinter.Entry(window)  # 创建输入框控件
entry1.place(relx=0.01, rely=0.08, relheight=0.06, relwidth=0.28)  # 放置输入框，并设置位置
entry1.insert(0, "ls /")  # 插入默认文字
but1 = tkinter.Button(window, text="运行指令", command=run_shell).place(relx=0.30, rely=0.08, relheight=0.06,
                                                                        relwidth=0.1)
but2 = tkinter.Button(window, text="清空屏幕", command=delete).place(relx=0.42, rely=0.08, relheight=0.06, relwidth=0.1)

entry2 = tkinter.Entry(window)  # 创建输入框控件
entry2.place(relx=0.01, rely=0.15, relheight=0.06, relwidth=0.28)  # 放置输入框，并设置位置
entry2.insert(0, "本地文件路径")  # 插入默认文字
entry3 = tkinter.Entry(window)  # 创建输入框控件
entry3.place(relx=0.30, rely=0.15, relheight=0.06, relwidth=0.28)  # 放置输入框，并设置位置
entry3.insert(0, "服务器文件路径")  # 插入默认文字
but4 = tkinter.Button(window, text="上传", command=up_file).place(relx=0.6, rely=0.15, relheight=0.06, relwidth=0.1)
but5 = tkinter.Button(window, text="下载", command=download_file).place(relx=0.72, rely=0.15, relheight=0.06,
                                                                        relwidth=0.1)

# 创建两个text文本框
text = tkinter.Text(window, width=75, height=60, undo=True, autoseparators=False)
text.place(relx=0.01, rely=0.3, relheight=0.65, relwidth=0.7)
text2 = tkinter.Text(window, width=75, height=60, undo=True, autoseparators=False)
text2.place(relx=0.72, rely=0.3, relheight=0.65, relwidth=0.27)
text2_default()
but6 = tkinter.Button(text2, text="OK", command=ok_file).place(relx=0.45, rely=0.9, relheight=0.06, relwidth=0.2)
# 进入主循环，显示主窗口
window.mainloop()
