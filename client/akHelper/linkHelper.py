import sys
import socket


class linkHelper:

    address = ('127.0.0.1', 65432)

    @staticmethod
    def link2server():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(linkHelper.address)
            print("pyAPKeep links to server: {}".format(s.getpeername()))
        except socket.error as msg:
            print(msg)
            sys.exit(1)
        return s

    @staticmethod
    def set_socket_address(ip, port):
        linkHelper.address = (ip, port)
