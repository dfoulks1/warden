#!/usr/bin/python3 -B

import subprocess

def order(machineID, cmd):
    try:
        command = ['systemd-nspawn', '--timezone', 'off', '-M', machineID]
        command.extend(cmd.split(' '))
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(e)
        
def daemonize(machineID):
    try:    
        subprocess.check_call(['systemctl', 'enable', 'systemd-nspawn@' + machineID + '.service'])
    except subprocess.CalledProcessError as e:
        print(e)
