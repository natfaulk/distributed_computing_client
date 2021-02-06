#!/usr/bin/python
import dotenv
dotenv.load_dotenv()

import time

from . import comms
from . import ping
from . import utils

from job import job


CLIENT_ID=utils.newID()

def start():
  print(f'Client ID: {CLIENT_ID}')
  c=comms.Comms(CLIENT_ID)
  running=False

  ping.begin(CLIENT_ID)

  while(1):
    j=c.getJob()

    if j['error']:
      print('Couldn\'t reach job server...')
      time.sleep(60)
      continue
    
    j=j['job']
    if j != {}:
      print(j)
      running=True
      out=job.run(j['params'])
      print('Job done')
      c.jobComplete(j['id'])

      print('uploading...')
      c.uploadJob(j['id'], out)

      running=False
    else:
      print('No jobs available')
      time.sleep(60)
