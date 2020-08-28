import csv
import os
import socket
import struct
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    f = []
    data = []
    size = []
    data_Size(size)
    read_csvData(f, data)

    HOST = '178.79.133.92'  # The remote host
    PORT = 5555  # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    send_csvData(s, data)
    end_time2 = receive_back_data(s)
    receive_cycle_time(s)
    data_representation(size, end_time2)


def data_Size(size):
    for i in range(1, 30):
        size.append((os.path.getsize('file' + str(i) + '.csv')) / 1000)


def read_csvData(f, data):
    for i in range(1, 30):
        f.append(open('file' + str(i) + '.csv', 'rb'))
        data.append(f[i - 1].readlines())

    for i in range(0, len(data)):
        data[i].append(bytes('END', 'utf-8'))

    for i in range(1, 30):
        f[i - 1].close()


def send_csvData(s, data):
    print("Sending data")

    while True:
        for line in data:
            for element in line:
                s.send(element)
        break

    print("Sending Complete")


def receive_back_data(s):
    print("Receiving back the data")

    max_buffer_size = 2048

    # Variables
    counter = 0
    start_time = time.time()
    end_time = []

    while True:
        client_message = s.recv(max_buffer_size)

        if bytes('END', 'utf-8') in client_message:
            end_time.append((time.time() - start_time))
            start_time = time.time()
            if counter == 28:
                break
            counter += 1

        if not client_message:
            break

    print("Done Receiving")

    return end_time


def receive_cycle_time(s):
    print("Receiving cycle times")

    # Variables
    end_time = []
    max_buffer_size = 4000

    while True:
        client_message = s.recv(max_buffer_size)
        if not client_message:
            break
        end_time.append(struct.unpack("f", client_message))

    print("Done Receiving")

    output_array = np.array(end_time)
    np.savetxt("End_Time_File.csv", output_array, delimiter=",")

    s.close()


def estimate_coefficients(x, y):
    # number of observations/points
    n = np.size(x)

    # mean of x and y vector
    m_x, m_y = np.mean(x), np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return b_0, b_1


def plot_regression_line(x, y, b):
    # predicted response vector
    y_pred = b[0] + b[1] * x

    # plotting the regression line
    plt.plot(x, y_pred, color="black")


def data_representation(size, end_time2):
    # Reading time file
    with open("End_Time_File.csv", "r") as file:
        end_time1 = file.readlines()
    file.close()

    for i in range(0, len(end_time1)):
        end_time1[i] = float(end_time1[i])

    # Cycle time
    cycle_time = []
    for i in range(0, len(end_time1)):
        cycle_time.append(end_time1[i] + end_time2[i])

    # Linear Regression
    b1 = estimate_coefficients(np.array(size), np.array(end_time1))
    b2 = estimate_coefficients(np.array(size), np.array(cycle_time))

    # Presenting the data
    fig = plt.figure()
    ax = fig.gca()
    df = pd.DataFrame(
        {'DataSize(KB)': size, 'Latency(s)': end_time1, 'CycleTime(s)': cycle_time})  # , 'CycleTime(s)': cycle_time
    plt.title("Transmission speed of 4G connection (KB/s)")
    plt.xlabel("Data  packet size (KB)")
    plt.plot('DataSize(KB)', 'Latency(s)', data=df, marker='o', markerfacecolor='red', markersize=6,
             color='red',
             linewidth=1)
    plt.plot('DataSize(KB)', 'CycleTime(s)', data=df, marker='o', markerfacecolor='blue', markersize=6,
             color='blue',
             linewidth=1)
    plot_regression_line(np.array(size), np.array(end_time1), b1)
    plot_regression_line(np.array(size), np.array(cycle_time), b2)
    plt.grid()
    plt.legend()
    plt.show()
    fig.savefig("TransmissionSpeed.png", dpi=300)
    fig.show()


if __name__ == "__main__":
    main()
