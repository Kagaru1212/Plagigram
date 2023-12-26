import socket
import time
import os

port = int(os.environ["POSTGRES_PORT"])  # 5432
host = os.environ["POSTGRES_HOST"]  # pgdb


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, port))
        s.close()
        break
    except socket.error as ex:
        time.sleep(1)
