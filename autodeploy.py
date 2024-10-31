import subprocess
import os
import time

os.system("sudo pkill gunicorn")
time.sleep(0.1)
os.system('cd /home/ubuntu/auric-fe')
os.system("gunicorn --bind=127.0.0.1:5020 app:app --daemon")
time.sleep(0.1)
os.system("ps ax|grep gunicorn")
os.system("sudo systemctl restart nginx")
time.sleep(0.1)
os.system("sudo systemctl status nginx")