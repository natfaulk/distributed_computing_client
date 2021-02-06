from src import client
from src import version

print('Distributed client version:', version.__version__)
client.start()
