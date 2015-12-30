if __name__ == '__main__' and __package__ is None:
  from os import sys, path
  sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import argparse, sys, socket, threading, json
from smartie.smartie import Smartie

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

smartie = Smartie()

def clientthread(conn, addr):
  #Sending message to connected client
  conn.send('Welcome to the server. Type something and hit enter\n'.encode()) #send only takes string

  #infinite loop so that function do not terminate and thread do not end.
  while True:
    # Receiving message from client
    raw_data = conn.recv(1024)

    if not raw_data:
      print('Connection to ' + address[0] + ':' + str(address[1]) + ' closed')
      break

    decoded_data = raw_data.decode()
    print('decoded_data')
    print(decoded_data)
    message = json.loads(decoded_data)
    print(repr(decoded_data))

    message_type = type(message).__name__

    print('Received message: ' + decoded_data)
    print('Message type: ' + message_type)
    # if message_type == 'dict':
    # if message_type == 'dict':
    for key, val in message.items():
      if 'backlight' in key.lower():
        if val.lower() == 'on':
          smartie.backlight_on()
        elif val.lower() == 'off':
          smartie.backlight_off()
      elif 'line' in key.lower():
        try:
          line = int(key[-1:])
        except ValueError:
          print('ERROR: ' + key + ' is not a number')

        print('writing line... ' + key + ': ' + val)
        smartie.write_line(val, line)

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
