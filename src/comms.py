import os

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

SERVER_PORT=os.getenv('SERVER_PORT')
SERVER_ADDR=os.getenv('SERVER_ADDR')
SERVER_USE_HTTP_HTTPS=os.getenv('USE_HTTP_HTTPS')

if SERVER_PORT is None:
  SERVER_PORT=3000

if SERVER_ADDR is None:
  SERVER_ADDR='127.0.0.1'

if SERVER_USE_HTTP_HTTPS.capitalize()=='HTTPS':
  SERVER_URL=f'https://{SERVER_ADDR}/'
else:
  SERVER_URL=f'http://{SERVER_ADDR}:{SERVER_PORT}/'

class Comms:
  def __init__(self, _client_id):
    self.id=_client_id

  def pingServer(self):
    r = requests.post(f'{SERVER_URL}ping', data={'id':self.id})
    print(r.text)

  def jobComplete(self, _jobID):
    params={
      'id':self.id,
      'task_id':_jobID
    }
    r = requests.post(f'{SERVER_URL}task_complete', data=params)
  
  def getJob(self):
    params={'id':self.id}
    r = requests.post(f'{SERVER_URL}get_task', data=params)
    return r

  def uploadJob(self, _jobID, _filename):
    payload = MultipartEncoder(
      fields={
        'id':self.id,
        'task_id':_jobID,
        'taskOutput': ('filename', open(_filename, 'rb'), 'application/binary')
      })

    r = requests.post(f'{SERVER_URL}upload_task', data=payload, headers={
      'Content-Type': payload.content_type
    })

    print('Upload response:', r.content)
