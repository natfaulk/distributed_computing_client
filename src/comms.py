import os

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

SERVER_PORT=os.getenv('SERVER_PORT')
SERVER_ADDR=os.getenv('SERVER_ADDR')

if SERVER_PORT is None:
  SERVER_PORT=3000

if SERVER_ADDR is None:
  SERVER_ADDR='127.0.0.1'

class Comms:
  def __init__(self, _client_id):
    self.id=_client_id

  def pingServer(self):
    r = requests.get(f'http://{SERVER_ADDR}:{SERVER_PORT}/ping', params={'id':self.id})
    print(r.text)

  def jobComplete(self, _jobID):
    params={
      'id':self.id,
      'job_id':_jobID
    }
    r = requests.get(f'http://{SERVER_ADDR}:{SERVER_PORT}/job_complete', params=params)
  
  def getJob(self):
    params={'id':self.id}
    r = requests.get(f'http://{SERVER_ADDR}:{SERVER_PORT}/get_job', params=params)
    return r

  def uploadJob(self, _jobID, _filename):
    payload = MultipartEncoder(
      fields={
        'id':self.id,
        'job_id':_jobID,
        'jobOutput': ('filename', open(_filename, 'rb'), 'application/binary')
      })

    r = requests.post(f'http://{SERVER_ADDR}:{SERVER_PORT}/upload_job', data=payload, headers={
      'Content-Type': payload.content_type
    })

    print('Upload response:', r.content)
