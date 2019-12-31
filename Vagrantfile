# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "generic/debian10"
  config.vm.network "private_network", type: "dhcp"

  # Share a folder with configuration to the guest VM
  config.vm.synced_folder ".", "/vagrant"

  # Provisioning script
  config.vm.provision "shell", path: "./provision.sh"

  # add more memory if needed
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end
end
