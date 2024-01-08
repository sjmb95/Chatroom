import socket
import select

header_length = 10

# socket configuration
IP = "127.0.0.1"
port = 1234
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, port))

server_socket.listen()



sockets_list = [server_socket]

clients = {}



def receive_message(client_socket):
    try :
        message_header = client_socket.recv(header_length)

        if not len(message_header):
            return False;

        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        pass




#
while True :
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    # go through all sockets that send notification
    for notified_socket in read_sockets:
        if notified_socket == server_socket: # new client  wants to connect
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(f" Accept new connection from {client_address[0]}  {client_address[1]} username : {user['data'].decode('utf-8')}");

        else : # when message is sent
            message = receive_message(notified_socket)
            if message is False :
                del clients[notified_socket]
                sockets_list .remove(notified_socket)
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                continue


            user = clients[notified_socket]
            print(f" Message received from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')}")

            # send message to all clients
            for client_socket in clients:
                if notified_socket != client_socket: # dont send message to self
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])


    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]















