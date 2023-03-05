import socket
import sys
import json

def socket_read(client, data_list):
    while True:
        data = client.recv(1024).decode()  # receive response
        data_list.append(json.loads(data))

    client.close()  # close the connection

if __name__ == '__main__':
    socket_read()