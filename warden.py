#!/usr/bin/python3

import sys
import argparse
import os
import yaml
import pydebootstrap
import pynspawn

def readYaml(profile):
    with open(profile, 'r') as ydata_file:
        try:
            ydata = yaml.safe_load(ydata_file)
            return ydata
        except yaml.YAMLError as e:
            print(e)


def main():
    parser = argparse.ArgumentParser('Create and Manage SystemD Jails')
    parser.add_argument('-n',
                        '--name',
                        help='Name of the chroot jail'
                        )
    parser.add_argument('-c',
                        '--create',
                        action='store_true',
                        help='Create a new Jail'
                        )
    parser.add_argument('-p',
                        '--profile',
                        help='vars file containing details about the chroot env'
                        )
    parser.add_argument('-r',
                        '--release',
                        action='store_true',
                        help='Release jail'
                        )
    parser.add_argument('-D',
                        '--daemonize',
                        action='store_true',
                        help='Run container as systemd unit'
                        )
    parser.add_argument('-o',
                        '--order',
                        help='Send comand or script to jail'
                        )
    parser.add_argument('-l',
                        '--list',
                        action='store_true',
                        help='List jails in the configured jailhouse'
                        )
    args = parser.parse_args()
    
    if args.list:
        pydebootstrap.list()
        sys.exit(0)
    elif args.release and args.name:
        pydebootstrap.release(args.name)
        sys.exit(0)
    elif args.order and args.name:
        pynspawn.order(args.name, args.order) 
        sys.exit(0)
    elif args.daemonize and args.name:
        pynspawn.daemonize(args.name)
        sys.exit(0)
    elif args.create and args.profile:
        profile = readYaml(args.profile)
        pydebootstrap.create(profile['conf'])
        if args.daemonize:
            pynspawn.daemonize(profile['conf']['name'])
    else:
        print("no actionable argument passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()

