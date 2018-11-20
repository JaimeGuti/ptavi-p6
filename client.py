#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys

try:
    METODO = sys.argv[1].upper()
    RECEPTOR = sys.argv[2].split("@")[0]
    IP = sys.argv[2].split("@")[1].split(":")[0]
    SIPPORT = int(sys.argv[2].split(":")[-1])

    # Contenido que vamos a enviar
    LINE = METODO + " sip:" + RECEPTOR + "@" + IP + " SIP/2.0\r\n\r\n"

    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.connect((IP, SIPPORT))

        if METODO == "INVITE":
            print("Enviando: " + LINE)
            my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
            data = my_socket.recv(1024)

        elif METODO == "BYE":
            print("Enviando: " + LINE)
            my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
            data = my_socket.recv(1024)

        mens_ack = data.decode('utf-8')
        if mens_ack == "SIP/2.0 100 Trying SIP/2.0 180 Ringing SIP/2.0 200 OK":
            ack_line = 'ACK' + " sip:" + RECEPTOR + "@"
            ack_line += IP + " SIP/2.0\r\n\r\n"
            print(ack_line)
            my_socket.send(bytes(ack_line, 'utf-8') + b'\r\n')
            data = my_socket.recv(1024)

        print('Recibido -- ', data.decode('utf-8'))
        print("Terminando socket...")

    print("Fin.")
except:
    sys.exit("Usage python3 client.py method receiver@IP:SIPport")
