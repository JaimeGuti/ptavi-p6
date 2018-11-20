#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import os

try:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    AUDIO = sys.argv[3]
except:
    sys.exit("Usage: python3 server.py IP port audio_file")


class EchoHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print("El cliente nos manda " + line.decode('utf-8'))
            diferente = line.decode('utf-8') != INVITE
            diferente += line.decode('utf-8') != BYE
            diferente += line.decode('utf-8') != ACK

            if line.decode('utf-8') == INVITE:
                self.wfile.write(b"SIP/2.0 100 Trying")
                self.wfile.write(b"SIP/2.0 180 Ringing")
                self.wfile.write(b"SIP/2.0 200 OK")

            elif line.decode('utf-8') == ACK:
                aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + AUDIO
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)

            elif line.decode('utf-8') == BYE:
                self.wfile.write(b"SIP/2.0 200 OK")

            elif diferente:
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed")

            else:
                self.wfile.write(b"SIP/2.0 400 Bad Request")

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', PORT), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Servidor apagado")
