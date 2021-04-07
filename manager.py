#!/usr/bin/env python3
import os
import time
import logging
import paramiko
from pathlib import Path

os.system('clear')

# logging the details and some errors
logger = paramiko.util.logging.getLogger()
handle = logging.FileHandler('report.log')

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handle.setFormatter(formatter)

logger.addHandler(handle)
logger.setLevel(logging.INFO)

# call the client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# select the machine and file
machine = int(input("Please Select your machine :"))
exec_file = input("Please Type file to deploy to the target machine :")
try:
    if machine == 1:
        start = time.perf_counter()
        # connect to host ip, port, username, password,
        client.connect('10.0.0.1', 22, 'worker_machine_1', 'worker_machine_1', timeout=4)
        # Preparing the target file to transfer and execute
        script_path = Path(exec_file).name
        run = open(script_path).read()
        stdin, stdout, stderr = client.exec_command(run)
        print(stdout.read().decode())
        error = stderr.read().decode()
        if error:
            logging.debug(error)
            logging.info('Error has occurred')
        end = time.perf_counter()
        print(f"Deployed target file in {end - start:0.4f} seconds")
        client.close()
        # repeating process on the other machine
    elif machine == 2:
        # start timer till the end to calculate the period
        start = time.perf_counter()
        client.connect('10.0.0.2', 22, 'worker_machine_2', 'worker_machine_2', timeout=4)
        script_path = Path(exec_file).name
        run = open(script_path).read()
        stdin, stdout, stderr = client.exec_command(run)
        # getting out result of the code that executed
        print(stdout.read().decode())
        error = stderr.read().decode()
        if error:
            logging.debug(error)
            logging.info('Error has occurred')
        end = time.perf_counter()
        print(f"Deployed target file in {end - start:0.4f} seconds")
        client.close()
    else:
        print("Couldn't connect to the host")
        raise logging.info(AttributeError)
except Exception as err:
    logging.debug(err)
    logging.info('Error Happened')
