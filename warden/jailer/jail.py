#!/usr/bin/python3

import subprocess
import os
import shutil


def create(args, jailhouse, conf):
    """ Check for the debootstrap command and create a jail with it """
    try:
        bootstrap_cmd_check = subprocess.run(['which', 'debootstrap'], stdout=subprocess.PIPE)
        bootstrap_cmd_check.check_returncode()
        bootstrap_cmd = bootstrap_cmd_check.stdout.decode('utf8').strip('\n')
    except subprocess.CalledProcessError as e:
        print(e)
         
    try:
        subprocess.check_call([bootstrap_cmd, '--variant', 'buildd', '--components', conf['components'], '--include', conf['includes'], '--arch', conf['arch'], conf['os'], jailhouse + args.name, conf['source']])
    except subprocess.CalledProcessError as e:
        print(e)

    try:
        subprocess.check_call(['systemd-nspawn', '--timezone', 'off', '-M', args.name, '/bin/echo', 'root:password', '|', '/usr/sbin/chpasswd'])
    except subprocess.CalledProcessError as e:
        print(e)


def order(args, jailhouse, cmd):
    try:
        command = ['systemd-nspawn', '--timezone', 'off', '-M', args.name]
        command.extend(cmd.split(' '))
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(e)

        
def daemonize(args):
    try:    
        subprocess.check_call(['systemctl', 'enable', 'systemd-nspawn@' + args.name + '.service'])
    except subprocess.CalledProcessError as e:
        print(e)


def release(args, jailhouse):
    """ unmount and remove chroot environment if it exists"""
    try:
        with open(os.devnull, 'w') as FNULL:
            subprocess.check_call(['machinectl', 'terminate', args.name], stdout=FNULL, stderr=FNULL)
    except subprocess.CalledProcessError as e:
        if str(e.returncode) != "1":
            print("There was a problem!")

    if os.path.isdir(jailhouse + "/" + args.name):
        shutil.rmtree(jailhouse + "/" + args.name)
    else:
        print("No jail by that name in the jailhouse")


def list(jailhouse):
    try:
        roster_check = subprocess.run(['ls', jailhouse], stdout=subprocess.PIPE)
        roster_check.check_returncode()
        roster = roster_check.stdout.decode('utf8')
    except subprocess.CalledProcessError as e:
        print(e)


    print(roster)
