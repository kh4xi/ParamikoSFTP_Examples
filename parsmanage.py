#!/usr/bin/env python3
import os
import time
import paramiko
import argparse
from pathlib import Path

# usage : python main.py --machine 1 --remoterun /home/file for executing remote bash file
os.system('clear')


if __name__ == "__main__":
    # parsing command line arguments
    parser = argparse.ArgumentParser(description='Server Manager')
    parser.add_argument('--machine', type=int, help='Choose Target machine')
    parser.add_argument('--remoterun', type=str, help='Transferring bash files and run on machine')
    args = parser.parse_args()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    if args.machine == 1:
        client.connect('192.168.1.21', 22, 'vm1', 'vm1', timeout=4)
    elif args.machine == 2:
        client.connect('192.168.1.22', 22, 'vm2', 'vm2', timeout=4)
    else:
        raise AttributeError('Please enter correct machine number')


        print("Please type the machine number correctly")


    start = time.perf_counter()
    # execute the BASH script
    only_script = Path(args.remoterun).name
    deploy_me = open(only_script).read()
    stdin, stdout, stderr = client.exec_command(deploy_me)
    # read the standard output and print it
    print(stdout.read().decode())
    # print errors if there are any
    err = stderr.read().decode()
    if err:
        print(err)
    # close the connection
    end = time.perf_counter()
    print(f"Deployed target file in {end - start:0.4f} seconds")

    client.close()