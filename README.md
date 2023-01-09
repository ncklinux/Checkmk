# Checkmk

Installing and monitoring with Checkmk free edition

## Motivation

I recently discovered [checkmk](https://checkmk.com) by two cool Computer Scientists with excellent and broad knowledge. I usually use [Zabbix](https://www.zabbix.com), [Icinga](https://icinga.com), [Nagios](https://www.nagios.org) etc, which I have worked on in the past, BTW are really great tools and I still use some of them today. So, since I saw [checkmk](https://checkmk.com) I can't take my eyes off it, I want to be all around it and get in depth with this amazing open source monitoring tool (give them a :star: on [GitHub](https://github.com/tribe29/checkmk/)). Let's have some fun and break the installation process into detailed pieces!

I will also provide some custom monitoring features with Shell Scripts and Python! They are coming soon in a second phase.

![Screenshot](./misc/screenshots/checkmk_dashboard_20230106.png)

## VM installation

Follow the [Vagrant](https://github.com/ncklinux/vagrant-ubuntu64) project of mine to spin up a new Ubuntu VM or use a ready-made [Vagrant Box](https://app.vagrantup.com/boxes/search) for convenience. Alternatively, you can use [Docker](https://github.com/ncklinux/docker-lemp) if you prefer (which I use daily). Also, you can choose [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (Vagrant actually does) and install [Ubuntu](https://ubuntu.com/download/server), [Debian](https://www.debian.org/download), [SLES](https://www.suse.com/products/server/) or [RedHat/CentOS](https://www.centos.org) or just any free/paid VM hosting, that actually can give you a virtual machine with those distributions, and of course with command line access.

## Ubuntu CLI

So, suppose you choose Vagrant, then [download](https://checkmk.com/download) and install checkmk (there's also an [official installation guide](https://docs.checkmk.com/latest/en/install_packages_debian.html)).

```bash
# Spin your VM
$ cd YOUR_VAGRANT_BOX
$ vagrant up
$ vagrant ssh

# Some maintenance work
$ sudo apt update && sudo apt upgrade -y
$ sudo apt autoremove -y
$ sudo apt clean

# Find out which release of Ubuntu you are using to download the correct free version of checkmk for your system https://checkmk.com/download
$ sudo lsb_release -a

# Retrieve the package
$ cd /tmp
$ wget https://download.checkmk.com/checkmk/2.1.0p18/check-mk-free-2.1.0p18_0.jammy_amd64.deb # Again, use your version here from https://checkmk.com/download

# Disk space check (will take 1.5GB more or less)
$ df -h

# Install the package and it's dependencies, the version in my case is as follows:
$ sudo apt install ./check-mk-free-2.1.0p18_0.jammy_amd64.deb -y

# OMD ;) The Open Monitoring Distribution https://docs.checkmk.com/latest/en/omd_basics.html
$ omd version # Should print out something like "OMD - Open Monitoring Distribution Version 2.1.0p18.cfe" with the actual version (2.1.0p18) I've used in this case

# Let's see first what it did on our system (i'm curious..)
$ sudo systemctl list-units | grep "check\|omd" # Just some services..
$ netstat -tupln # Runs with Apache on port 5000
$ which omd # The binary..
$ ls -ls / # A symlink..
# lrwxrwxrwx 1 root root 8 Jan 4 19:58 omd -> /opt/omd
$ ls -ls /opt/omd/ # Here are Apache, possible sites (instances I guess) and versions..
# OK, very nice!

#Let's create our first monitoring site now, the instance (and you can have of multiple of them)
$ omd create mymonitoring # You can replace mymonitoring your own name and should print something like the following:
# Adding /opt/omd/sites/mymonitoring/tmp to /etc/fstab.
# Creating temporary filesystem /omd/sites/mymonitoring/tmp...OK
# Updating core configuration...
# Generating configuration for core (type cmc)...
#
# WARNING: The number of configured checkers is higher than the number of available CPUs. To avoid unnecessary context switches, the number of checkers should be limited to the number of CPUs. Recommended number of checkers: 1
# Starting full compilation for all hosts Creating global helper config...OK
#  Creating cmc protobuf configuration...OK
# Executing post-create script "01_create-sample-config.py"...OK
# Created new site mymonitoring with version 2.1.0p18.cfe.
#
#   The site can be started with omd start mymonitoring.
#   The default web UI is available at http://vagrant/mymonitoring/
#
#   The admin user for the web applications is cmkadmin with password: YOUR_PASSWORD_WILL_APPEAR_HERE
#   For command line administration of the site, log in with 'omd su mymonitoring'.
#   After logging in, you can change the password for cmkadmin with 'cmk-passwd cmkadmin'.

$ omd start mymonitoring # It will produce the following output:
# Temporary filesystem already mounted
# Starting agent-receiver...OK
# Starting mkeventd...OK
# Starting liveproxyd...OK
# Starting mknotifyd...OK
# Starting rrdcached...OK
# Starting cmc...OK
# Starting apache...OK
# Starting dcd...OK
# Starting redis...OK
# Initializing Crontab...OK

# List all available commands
$ omd

# Check status
$ omd status mymonitoring
# agent-receiver: running
# mkeventd:       running
# liveproxyd:     running
# mknotifyd:      running
# rrdcached:      running
# cmc:            running
# apache:         running
# dcd:            running
# redis:          running
# crontab:        running
# -----------------------
# Overall state:  running

# List all sites
$ omd sites
# SITE             VERSION          COMMENTS
# mymonitoring     2.1.0p18.cfe     default version

# Man page ;)
man omd
# OMD(8) System Manager's Manual OMD(8)
#
# NAME
#       omd - admin interface for OMD, the Open Monitoring Distribution
#
# SYNOPSIS
#        omd [command [site...]  ]
#
# DESCRIPTION
#        OMD  -  the Open Monitoring Distribution is something really new. OMD bundles existing open source software to ease the installation procedure of Nagios and many important addons like NagVis, PNP4Nagios, rrdtool, nagios-plug‐
#        ins, Check_MK, MK Livestatus, Dokuwiki, NSCA, check_nrpe and others.
#
#        OMD supports:
#
#        - multiple versions of OMD installed in parallel
#        - multiple instances of Nagios running in parallel (so called "sites")
#
#        omd is the administration interface for creating and maintaining sites within OMD - the open monitoring distribution.
#
# COMMANDS
#        omd help
#               Show short summary of available commands.
# ...
```

Then specify a static IP address in [Vagrant](https://developer.hashicorp.com/vagrant/docs/networking/private_network) file e.g. `config.vm.network "private_network", ip: "192.168.57.10"` and reboot, make sure that the IP does not collide with any other machines on the same network (use [nmap](https://wiki.archlinux.org/title/nmap) or [Angry IP Scanner](https://angryip.org) for that).

On reboot `omd` will start automatically but it's always good to check the status `omd status mymonitoring`.

In the meantime it's nice to know more about checkmk's [ports](https://docs.checkmk.com/latest/en/ports.html).

Visit the monitoring UI at [http://192.168.57.10/mymonitoring/](http://192.168.57.10/mymonitoring/) and login (the default username is `cmkadmin` and the password is in the `omd create mymonitoring` output of the example above).

![Screenshot](./misc/screenshots/checkmk_login.png)

## checkmk UI

The first thing to do is to monitor the VM itself, navigate to "Setup->Agents(Windows, Linux, Solaris, AIX)" and select the Ubuntu agent `check-mk-agent_2.1.0p18-2ec94b9ec2f2a91a_all.deb` (your file may differ in the version), copy the agent to Vagrant VM:

```bash
$ vagrant plugin install vagrant-sc
$ vagrant scp /home/YOUR_USER/Downloads/check-mk-agent_2.1.0p18-2ec94b9ec2f2a91a_all.deb :~/.
$ vagrant ssh
$ sudo apt install ./check-mk-agent_2.1.0p18-2ec94b9ec2f2a91a_all.deb
$ sudo systemctl list-units | grep "check\|omd"
# opt-omd-sites-mymonitoring-tmp.mount   loaded active mounted   /opt/omd/sites/mymonitoring/tmp
# check-mk-agent-async.service           loaded active running   Checkmk agent - Asynchronous background tasks
# check-mk-free-2.1.0p18.service         loaded active exited    LSB: OMD sites
# omd.service                            loaded active exited    Checkmk Monitoring
# check-mk-agent.socket                  loaded active listening Local Checkmk agent socket
```

In order to add the VM to the monitoring system do the following:

1. Click on "Setup->Hosts->Add Host" and add your hostname (to find your FQDN use `hostname -f`)
2. Add the IP address `192.168.57.10` (the IP can be optional if you used your real FQDN)
3. Click on "Save & go to service configuration" and you should start receiving all discovered services
4. Use the + or - buttons to choose which ones to monitor or click "Accept all"
5. At the top right you can see your "changes", which you have to apply manually, click on "Activate on selected sites"

That's all, then you can check everything from the "Overview" panel, click on the "Hosts" (on number 1) and a table with the status of the VM will appear.

For additional VMs, repeat the same steps from 1-5, copy and install the agent and on the previous VM (the one with checkmk installed), simply add the host.

![Screenshot](./misc/screenshots/checkmk_new_host.png)

## Vagrant

Use the following commands to manage multiple VMs

```bash
$ vagrant up
$ vagrant global-status
# id       name    provider   state    directory
# -------------------------------------------------------------------
# mpc777i  master  virtualbox running  /home/YOUR_USER/Checkmk
# mpc778i  node    virtualbox running  /home/YOUR_USER/Checkmk

# The above shows information about all known Vagrant environments
# on this machine. This data is cached and may not be completely
# up-to-date (use "vagrant global-status --prune" to prune invalid
# entries). To interact with any of the machines, you can go to that
# directory and run Vagrant, or you can use the ID directly with
# Vagrant commands from any directory. For example:
# "vagrant destroy mpc777i"

# SSH to the master VM (by using the name)
$ vagrant ssh master

# SSH to the node VM
$ vagrant ssh node

# Shutdown both VMs
$ vagrant halt
# ==> node: Attempting graceful shutdown of VM...
# ==> master: Attempting graceful shutdown of VM...
```

## License

MIT

## Disclaimer

This project is distributed FREE & WITHOUT ANY WARRANTY. Report any bugs or suggestions here as an [issue](https://github.com/ncklinux/Checkmk/issues/new).

## Contributing

Please read the [contribution](https://github.com/ncklinux/.github/blob/main/CONTRIBUTING.md) guidelines.

## Commit Messages

This repository follows the [Conventional Commits](https://www.conventionalcommits.org) specification, the commit message should never exceed 100 characters and must be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Powered by

<img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/unix/unix-original.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bash/bash-original.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/ssh/ssh-original-wordmark.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vagrant/vagrant-original.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nginx/nginx-original.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/apache/apache-original-wordmark.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/php/php-original.svg" /><img height="33" style="margin-right: 3px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-plain-wordmark.svg" />
