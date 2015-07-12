import argparse, sys, socket, threading, json
from lcd import *

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--host')
parser.add_argument('-p', '--port', type=int)
args = parser.parse_args()

HOST = args.host or ''
PORT = args.port or 8089

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
    raw_data = conn.recv(1024)

    if not raw_data:
      print('Connection to ' + address[0] + ':' + str(address[1]) + ' closed')
      break

    decoded_data = raw_data.decode()
    print('decoded_data')
    print(decoded_data)
    data = json.loads(decoded_data)
    print(repr(decoded_data))

    print('Received message: ' + decoded_data)
    for key, val in data.items():
      if 'line' in key.lower():
        try:
          line = int(key[-1:])
        except ValueError:
          print('ERROR: ' + key + ' is not a number')

        print('writing line... ' + key + ': ' + val)
        write_line(val, line)

    reply = 'You sent: ' + decoded_data
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
