```sh
sudo apt-get install python-pip
pip install pyserial

# Run in foreground
python3 server.py

# Run in background
python3 server.py > ./server.log 2>&1 &
```
