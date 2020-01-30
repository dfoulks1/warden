#!/usr/bin/python3 -B

import subprocess
import os
import shutil
from . import config


def create(conf):
    """ Check for the debootstrap command and create a debian based jail from source.
        Requires:
            conf:
              components:   <comma separated list of repos to add>
              includes:     <comma separated list of packages to install
              arch:         architecture (currently supported amd64)
              os:           <debian based operating system flavor>
              source:       <URL to fetch the operating system files from>
              name:         <machine name>
    """
    try:
        bootstrap_cmd_check = subprocess.run(['which', 'debootstrap'], stdout=subprocess.PIPE)
        bootstrap_cmd_check.check_returncode()
        bootstrap_cmd = bootstrap_cmd_check.stdout.decode('utf8').strip('\n')
    except subprocess.CalledProcessError as e:
        print(e)
         
    try:
        subprocess.check_call([bootstrap_cmd, '--variant', 'buildd', '--components', conf['components'], '--include', conf['includes'], '--arch', conf['arch'], conf['os'], config.jailhouse + conf['name'], conf['source']])
    except subprocess.CalledProcessError as e:
        print(e)


def release(name):
    """ machinectl terminate the environment if it exists, and remove the debootstrapped directory"""
    try:
        with open(os.devnull, 'w') as FNULL:
            subprocess.check_call(['machinectl', 'terminate', name], stdout=FNULL, stderr=FNULL)
    except subprocess.CalledProcessError as e:
        if str(e.returncode) != "1":
            print("There was a problem!")

    if os.path.isdir(config.jailhouse + name):

        shutil.rmtree(config.jailhouse + name)
    else:
        print("No jail by that name in the jailhouse")


def list():
    try:
        roster_check = subprocess.run(['ls', config.jailhouse], stdout=subprocess.PIPE)
        roster_check.check_returncode()
        roster = roster_check.stdout.decode('utf8')
    except subprocess.CalledProcessError as e:
        print(e)

    print(roster)
