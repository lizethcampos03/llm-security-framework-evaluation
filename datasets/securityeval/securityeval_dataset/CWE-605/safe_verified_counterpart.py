from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def echoServer(port, bind_address='127.0.0.1'):
    '''
    Create a socket server that echos back the message sent.
    '''
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 0)
    s.bind((bind_address, port))
    s.listen(1)
    conn, addr = s.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.send(data)
    conn.close()