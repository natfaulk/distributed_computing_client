import os
import socket

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from . import version

SERVER_PORT=os.getenv('SERVER_PORT')
SERVER_ADDR=os.getenv('SERVER_ADDR')
SERVER_USE_HTTP_HTTPS=os.getenv('USE_HTTP_HTTPS')

if SERVER_PORT is None:
  SERVER_PORT=3000

if SERVER_ADDR is None:
  SERVER_ADDR='127.0.0.1'

if SERVER_USE_HTTP_HTTPS is not None and SERVER_USE_HTTP_HTTPS.upper().strip()=='HTTPS':
  SERVER_URL=f'https://{SERVER_ADDR}/'
else:
  SERVER_URL=f'http://{SERVER_ADDR}:{SERVER_PORT}/'

print(SERVER_URL)

class Comms:
  def __init__(self, _client_id):
    self.id=_client_id

  def pingServer(self):
    params = {
      'id':self.id,
      'hostname': socket.gethostname(),
      'clientVersion': version.__version__
    }

    try: 
      r = requests.post(f'{SERVER_URL}ping', data=params)
      print(r.text)
    except:
      print('Error pinging server')

  def jobComplete(self, _jobID):
    params={
      'id':self.id,
      'task_id':_jobID
    }
    try:
      r = requests.post(f'{SERVER_URL}task_complete', data=params)
    except:
      print('Error sending job complete')

  def getJob(self):
    params={'id':self.id}

    out = {'error':False, 'job':{}}

    try:
      r = requests.post(f'{SERVER_URL}get_task', data=params)
      out['job'] = r.json()
    except:
      print('Error getting job')
      # an error currently will return the same as no job available
      out['error'] = True
    
    return out

  def uploadJob(self, _jobID, _filename):
    payload = MultipartEncoder(
      fields={
        'id':self.id,
        'task_id':_jobID,
        'taskOutput': ('filename', open(_filename, 'rb'), 'application/binary')
      })

    try:
      r = requests.post(f'{SERVER_URL}upload_task', data=payload, headers={
        'Content-Type': payload.content_type
      })
      print('Upload response:', r.content)
    
    except:
      print('Error uploading job')

