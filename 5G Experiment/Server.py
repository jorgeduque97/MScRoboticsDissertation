import csv
import os
import socket
import struct
import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    f = []
    size = []
    end_time, data, connection = start_server(size)
    send_back_data(data, connection)
    send_cycle_time(connection, end_time)


def start_server(size):
    host = ''
    port = 5555
    max_buffer_size = 2048  # 1024

    SocketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SocketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_ip = socket.gethostbyname(host)
    print("Socket created")

    try:
        SocketServer.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    SocketServer.listen(5)  # queue up to 5 requests
    print("Socket now listening")

    # Establish connection
    connection, address = SocketServer.accept()
    ip, port = str(address[0]), str(address[1])
    print("Connected with " + ip + ":" + port)
    print("Receiving data")

    # Variables
    counter = 0
    start_time = time.time()
    end_time = []
    data = []

    while True:
        client_message = connection.recv(max_buffer_size)
        data.append(client_message)

        if bytes('END', 'utf-8') in client_message:
            end_time.append((time.time() - start_time))
            start_time = time.time()
            if counter == 28:
                break
            counter += 1

        if not client_message:
            break

    print("Done Receiving")

    return end_time, data, connection


def send_back_data(data, connection):
    print("Sending back data")

    while True:
        for element in data:
            connection.send(element)
        break

    print("Sending back Complete")


def send_cycle_time(connection, end_time):
    print("Sending cycle times")
    time.sleep(1)

    while True:
        for element in end_time:
            connection.send(struct.pack("f", element))
            time.sleep(0.3)
        break

    print("Sending Complete")

    connection.close()


if __name__ == "__main__":
    main()
