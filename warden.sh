#!/bin/bash

JAILHOUSE="/home/dfoulks/jailhouse"
helpme="
$0
manages an organization of chroot jails located in configurable: JAILHOUSE.
Currently: $JAILHOUSE

Usage:
	warden lockup <jailname> 	-- create a chroot jail in $JAILHOUSE/<jailname>
	
	warden visit <jailname> 	-- chroot to the jail name.
	      - on the first visit 
		source the reform.sh 
		file.
	
	warden release <jailname> 	-- umount and remove jail in $JAILHOUSE/<jailname>
	
	warden roster 			-- list all of the current jails

	warden reform			-- source an activation script"

[ -z "$1" ] && echo "$helpme" && exit 0 
action=$1
shift
jailcell="$JAILHOUSE/$1"
shift
order=$@


function lockemup() {
	[ -d $jailcell ] && letemgo

	mkdir $jailcell

	$(which debootstrap) --variant buildd --arch amd64 --include=build-essential,python3,curl,wget,systemd,git,net-tools --components=main,universe disco $jailcell http://archive.ubuntu.com/ubuntu
        systemd-nspawn -D $jailcell -M disco
}


letemgo() {
	if [ check_jailhouse ]; then
		sudo umount $jailcell/proc
		sudo rm -rf $jailcell 
	fi
}


visitjail() {
	if [ check_jailhouse ]; then	
		sudo chroot $jailcell
	fi
}

roster() {
	if [ -z "$(ls $JAILHOUSE)" ]; then
		echo "$JAILHOUSE is empty"
	else
		echo `ls $JAILHOUSE`
	fi
}


check_jailhouse() {
	if [ -d $jailcell ]; then
		return true
	else
		return false
	fi
}

case "$action" in
	lockup)
		lockemup
		;;
	release)
		letemgo
		;;
	roster)
		roster
		;;
	visit)
		visitjail 
		;;
	order)
		sudo chroot $jailcell $order
		;;
	--help|help|*)
		echo "$helpme"
		;;
esac
