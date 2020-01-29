#!/usr/bin/python3

import sys
import argparse
import os
import yaml
import config
import jailer.jail as jail

def readYaml(profile):
    with open(profile, 'r') as ydata_file:
        try:
            ydata = yaml.safe_load(ydata_file)
            return ydata
        except yaml.YAMLError as e:
            print(e)
def main():


    parser = argparse.ArgumentParser('Manage chroot environments')
    parser.add_argument('-n',
                        '--name',
                        help='Name of the chroot jail'
                        )
    parser.add_argument('-j',
                        '--jail',
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
    parser.add_argument('-v',
                        '--verbose',
                        help='Print messages'
                        )
    parser.add_argument('-l',
                        '--list',
                        action='store_true',
                        help='List jails in the configured jailhouse'
                        )
    args = parser.parse_args()
    
    jailhouse = config.jail
    osdata = readYaml("resources/os.yaml")
    moddata = readYaml("resources/mods.yaml")
    if args.list:
        jail.list(jailhouse)
        sys.exit(0)
    elif args.release and args.name:
        jail.release(args, jailhouse)
        sys.exit(0)
    elif args.order and args.name:
        jail.order(args, jailhouse, args.order) 
        sys.exit(0)
    
    if not args.profile:
        print("No profile provided, exiting...")
        sys.exit(1)

    profile = readYaml(args.profile)
    conf = osdata[profile['os']]

    if args.jail and args.name:
        jail.create(args, jailhouse, conf['conf'])
        if args.daemonize:
            jail.daemonize(args, jailhouse)
#        if len(profile['modules']) > 0:
#            for module in profile['modules']:
#                for command in moddata[module]:
#                    jail.order(args, jailhouse, command)

    else:
        print('Error: Insufficient Information Provided')
        print(parser.print_help())
        print('\nJail, Release, and Deputize functions require a Name')
        print('\nList does not require a name')
        sys.exit(0)

if __name__ == "__main__":
    main()

