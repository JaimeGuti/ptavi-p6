#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import os

try:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    AUDIO = sys.argv[3]
except(IndexError, ValueError):
    sys.exit("Usage: python3 server.py IP port audio_file")


class EchoHandler(socketserver.DatagramRequestHandler):

    def handle(self):

        line = self.rfile.read().decode('utf-8').split()[0]
        print("El cliente nos manda " + line)
        diferente = (line != "INVITE") or (line != "BYE") or (line != "ACK")

        if line == "INVITE":
            self.wfile.write(b"SIP/2.0 100 Trying")
            self.wfile.write(b" SIP/2.0 180 Ringing")
            self.wfile.write(b" SIP/2.0 200 OK")

        elif line == "ACK":
            aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + AUDIO
            print("Vamos a ejecutar", aEjecutar)
            os.system(aEjecutar)

        elif line == "BYE":
            self.wfile.write(b"SIP/2.0 200 OK")

        elif diferente:
            self.wfile.write(b"SIP/2.0 405 Method Not Allowed")

        else:
            self.wfile.write(b"SIP/2.0 400 Bad Request")

            
if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', PORT), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Servidor apagado")
