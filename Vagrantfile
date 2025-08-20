Vagrant.configure("2") do |config|
  # Define Master Node
  config.vm.define "master" do |master|
    master.vm.box = "ubuntu/bionic64"
    master.vm.network "private_network", ip: "192.168.56.10"
    master.vm.hostname = "master"
    master.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.name = "master"
    end

    # Enable rsync for syncing a folder between the host and VM
    master.vm.synced_folder "./host_folder", "/vagrant_data", type: "rsync"
  end

  # Define Worker 1
  config.vm.define "worker1" do |worker|
    worker.vm.box = "ubuntu/bionic64"
    worker.vm.network "private_network", ip: "192.168.56.11"
    worker.vm.hostname = "worker1"
    worker.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.name = "worker1"
    end

    # Enable rsync for syncing a folder between the host and VM
    worker.vm.synced_folder "./host_folder", "/vagrant_data", type: "rsync"
  end

  # Define Worker 2
  config.vm.define "worker2" do |worker|
    worker.vm.box = "ubuntu/bionic64"
    worker.vm.network "private_network", ip: "192.168.56.12"
    worker.vm.hostname = "worker2"
    worker.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.name = "worker2"
    end

    # Enable rsync for syncing a folder between the host and VM
    worker.vm.synced_folder "./host_folder", "/vagrant_data", type: "rsync"
  end
end
