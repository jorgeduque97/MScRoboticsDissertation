import socket
import sys
import traceback
from threading import Thread
from PathPlanning import PathPlanning

# RobotStudio Coordinates
RobotCoordinates = "1338.534912367-1396.107534.689"


def main():
    Path = PathPlanning()
    mypath = Path.path()
    start_server(mypath)


def start_server(mypath):
    host = ''
    port = 5555
    ThreadCount = 0

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

    while True:
        connection, address = SocketServer.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        try:
            if ThreadCount == 0:
                t1 = Thread(target=client_path_planning, args=(connection, ip, port, mypath)).start()
            elif ThreadCount == 1:
                t2 = Thread(target=client_thread_receive, args=(connection, ip, port)).start()
            else:
                t3 = Thread(target=client_thread_send, args=(connection, ip, port)).start()
            ThreadCount += 1
        except:
            print("Thread did not start.")
            traceback.print_exc()


def client_thread_receive(connection, ip, port, max_buffer_size=5120):
    is_active = True

    while is_active:
        client_message = connection.recv(max_buffer_size)
        client_message = str(client_message, 'utf-8')
        if client_message == "Controller 1 stopped":
            connection.shutdown(1)
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            is_active = False
        else:
            print("Client " + ip + " in port " + port + ": " + client_message)


def client_thread_send(connection, ip, port, max_buffer_size=5120):
    is_active = True

    while is_active:
        client_message = connection.recv(2048)
        client_message = str(client_message, 'utf-8')
        if not client_message:
            pass
        if client_message == "Controller 2 stopped":
            connection.shutdown(1)
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            is_active = False
            break
        else:
            print("Client " + ip + " in port " + port + ": " + client_message)
        connection.send(str.encode(RobotCoordinates))
        print("Sending target coordinates to Robot 2")


def client_path_planning(connection, ip, port, path, max_buffer_size=15120):
    is_active = True
    i = 0

    while is_active:
        client_message = connection.recv(max_buffer_size)
        client_message = str(client_message, 'utf-8')
        if not client_message:
            pass
        if client_message == "End of separation process":
            connection.shutdown(1)
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            is_active = False
            break
        else:
            print("Client " + ip + " in port " + port + ": " + client_message)
        connection.send(str.encode(path[i]))
        print("Sending element " + str(i + 1) + " of the path: " + path[i])
        i += 1


if __name__ == "__main__":
    main()
