import threading
import time

from . import comms

PING_INTERVAL=60

def begin(_client_id):
  x=threading.Thread(target=pingThread, args=(_client_id,), daemon=True)
  x.start()

def pingThread(_client_id):
  print('Ping thread began...')
  c=comms.Comms(_client_id)
  while(1):
    c.pingServer()
    time.sleep(PING_INTERVAL)


