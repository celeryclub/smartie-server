import sys
import socket
import threading

from lcd import *
# from smartie_lcd import * as lcd

HOST = '' # All network interfaces
PORT = 8089

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
  server.bind((HOST, PORT))
except socket.error as msg:
  print('Failed to bind to port ' + str(PORT) + '. ' + str(msg))
  sys.exit()

print('Socket bind complete')

server.listen(10) # Maximum 10 connections
print('Socket now listening')

def clientthread(conn, addr):
  #Sending message to connected client
  conn.send('Welcome to the server. Type something and hit enter\n'.encode()) #send only takes string

  #infinite loop so that function do not terminate and thread do not end.
  while True:
    # Receiving from client
    data = conn.recv(1024).decode()
    if not data:
      print('Connection to ' + address[0] + ':' + str(address[1]) + ' closed')
      break

    print('Received message: ' + data)
    write_line(data)

    reply = 'You sent: ' + data
    conn.sendall(reply.encode())

  #came out of loop
  conn.close()

try:
  while True:
    connection, address = server.accept()
    print('Connected with ' + address[0] + ':' + str(address[1]))

    threading.Thread(
      target=clientthread,
      args=(connection, address)
    ).start()
except KeyboardInterrupt:
  print('Closing connection')
  server.close()
