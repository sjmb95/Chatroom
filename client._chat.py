import socket
import errno
import select
import sys

# socket configuration
ip = "127.0.0.1"
port = 1234
header_length = 10
my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((ip, port))
client_socket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{header_length}}".encode("utf-8")
client_socket.send(username_header + username)




while True :
    message = input(f"{my_username} > ")
    # encode the message and send it
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):<{header_length}}".encode("utf-8")
        client_socket.send(message_header + message)


    try:
        while True:

            username_header = client_socket.recv(header_length)
            if not len(username_header):
                print("connection has been closed")
                sys.exit()

            # getting the length of username within the header
            username_length = int(username_header.decode("utf-8").strip())
            # getting the username
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(header_length)
            # getting length of message within message header
            message_length = int(message_header.decode("utf-8").strip())

            message = client_socket.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading Error : ", str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General Error', str(e))
        sys.exit()


