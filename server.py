import socket
import select

IP = "0.0.0.0"
PORT = 5353

server = socket.socket()

server.bind((IP, PORT))
server.listen(2)
client_list = []
messages_to_send = []
names={}

def send_waiting_message(wlist):
    for message in messages_to_send:
        src_client, msg = message
        for client in wlist:
            if client != src_client:
                client.send(msg)

        messages_to_send.remove(message)


while True:
    rlist, wlist, xlist = select.select([server] + client_list, client_list, [])
    for current_socket in rlist:

        if current_socket is server:
            (new_socket, address) = server.accept()
            client_list.append(new_socket)
            print("New connection with client!")
        else:
            data = current_socket.recv(1024)
            print (data.decode("UTF-8"))
            # data = current_socket.recv(rlist, wlist, xlist)
            if data.decode("UTF-8") == "EXIT":
                client_list.remove(current_socket)
                print("Connection Closed")




            else:
                messages_to_send.append((current_socket, b"" + data))
    send_waiting_message(wlist)
