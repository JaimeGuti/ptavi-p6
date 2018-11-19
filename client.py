#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.
try:
    METODO = sys.argv[1].upper()
    RECEPTOR = sys.argv[2].split("@")[0]
    IP = sys.argv[2].split("@")[1].split(":")[0]
    SIPPORT = int(sys.argv[2].split(":")[-1])

    # Contenido que vamos a enviar
    LINE = '¡Hola mundo!'

    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.connect((IP, SIPPORT))

        print("Enviando: " + LINE)
        a = bytes(METODO, 'utf-8') + bytes(RECEPTOR, 'utf-8') + b'\r\n\r\n'
        my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)

        print('Recibido -- ', data.decode('utf-8'))
        print("Terminando socket...")

        if METODO == "INVITE":
            print("ok invite")

    print("Fin.")
except:
    sys.exit("Usage python3 client.py method receiver@IP:SIPport")
