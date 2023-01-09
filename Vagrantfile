# -*- mode: ruby -*-
# vi: set ft=ruby :

# Define multiple VMs https://developer.hashicorp.com/vagrant/docs/multi-machine
Vagrant.configure("2") do |config|

    # Common configuration
    config.vm.box = "vagrant-ubuntu64"
    config.vm.provision :shell, inline: <<-SHELL
        apt update
        apt -y upgrade
        apt -y autoremove
        apt clean
        apt -y install git zsh
    SHELL
    config.vm.provision :shell, privileged: false, inline: "git clone https://github.com/ohmyzsh/ohmyzsh.git ~/.oh-my-zsh"
    config.vm.provision :shell, privileged: false, inline: "cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc"
    config.vm.provision :shell, inline: "chsh -s /bin/zsh vagrant"

    # Individual configurations
    config.vm.define "master" do |master|
        master.vm.hostname = "master"
        master.vm.network "private_network", ip: "192.168.57.10"
        master.vm.network "forwarded_port", guest: 5000, host: 5000, auto_correct: true
        master.vm.provision :shell, inline: "apt -y install apache2"
    end

    config.vm.define "node" do |node|
        node.vm.hostname = "node"
        node.vm.network "private_network", ip: "192.168.57.11"
        node.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: true
        node.vm.network "forwarded_port", guest: 443, host: 8043, auto_correct: true
        node.vm.provision :shell, inline: "apt -y install nginx"
    end
end
