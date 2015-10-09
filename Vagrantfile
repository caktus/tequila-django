# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"

#  config.vm.network :private_network, ip: "33.33.33.10"

  config.vm.provision "ansible" do |ansible|
    ansible.groups = {
      "web" => ["default"],
      "worker" => ["default"],
      "db" => ["default"]
    }
    ansible.extra_vars = { }
    ansible.playbook = "site.yml"
#    ansible.verbose = 'vv'
    ansible.roles_path = "tequila/roles"
  end
end
