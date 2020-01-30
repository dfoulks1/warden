# Warden Utility

Create and manage systemd-machines with debootstrap and systemd-nspawn.

*NOTE* Due to the nature of this script and its intended function, it should always be run as root.

The utility is capable of creating a fully customizable, bootable version of the (hopefully, systemd compatible) operating system defined in the profile.
Unlike a basic chroot environmnent, Wardens Jails also use systemd to initialize a new instance of systemd in that container as PID 1. Actors inside of the
Jailed container have no cognizance of the systemd processes running on the Parent machine.

## Compatability with Systemd.machined and machinectl

The Pydebootstrap module will create a machine image in the default systemd-mahined location (/var/lib/machines). For the most part these machines remain
in a 'poweredoff' state, according to machinectl. Machines can be brought online and used with machinectl, though for most purposes it's not really recommended,
machines held by machinectl will repond as 'busy' if a command is sent to it via warden.

Otherwise machines created with warden function exactly as machines created with machinectl would work.

## Contained Modules:
### PyDebootstrap

This module wraps around the debootstrap utility that has existed (almost) forever. There are several functions in the pydeboostrap module including:
    - create
    - release
    - list

#### Create
pydebootstrap.create() requires a configuration file like this one:

'''
conf:
  os: 'bionic'
  arch: 'amd64'
  components: 'main,universe'
  includes: 'build-essential,python3,curl,wget,systemd,git,net-tools,systemd-sysv,dbus,vim'
  source: 'http://archive.ubuntu.com/ubuntu'
  name: 'bionic'
'''

to be passed to it as profile. The machine that the profile describes does not necessarily have to match the OS of the Parent Machine.

#### Release and List
pydebootstrap.release() requires only the name of the virtual machine that you wish to terminate
pydebootstrap.list() will print the names of each of the directories in /var/lib/mahines

### PyNspawn

This module wraps around the systemd-nspawn command to take advantage of the excellent process jailing that is provided by this.
The module contains two functions:
    - order
    - daemonize


#### Order
pynspawn.order allows a user to send a command directly to the jail environment and will return all output


#### Daemonize
pynspawn.daemonize will start the jail and keep it up if we need a jail with networking and availability.

