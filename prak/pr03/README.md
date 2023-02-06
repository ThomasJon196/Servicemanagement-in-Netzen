## Task 1 - Setup ansible

### a) Ansible version: (installed via python virtual env.)

```
ansible [core 2.13.5]
  config file = None
  configured module search path = ['/home/thomas/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/thomas/Documents/Studies/Modules/ServicemanagementInNetzen/servmgmt-ws22/ansible/venv/lib/python3.10/site-packages/ansible
  ansible collection location = /home/thomas/.ansible/collections:/usr/share/ansible/collections
  executable location = /home/thomas/Documents/Studies/Modules/ServicemanagementInNetzen/servmgmt-ws22/ansible/venv/bin/ansible
  python version = 3.10.6 (main, Aug 10 2022, 11:40:04) [GCC 11.3.0]
  jinja version = 3.1.2
  libyaml = True
```

### b) Ping with ansible:

- **Ping localhost**

  `$ ansible all -i "localhost," --connection=local -m ping`

  - `ansible all` - Run commands against all hosts

  - `-m ping` - Used ansible module

  - `--connection=local` - Run commands on the local server, not over SSH

  - `-i "localhost,"` - Specify inventory host path or comma separated host list.

  Result:

  ```bash
  localhost | SUCCESS => {
      "ansible_facts": {
          "discovered_interpreter_python": "/usr/bin/python3"
      },
      "changed": false,
      "ping": "pong"
  }
  ```

  What happens on execution:

  1. Ansible tries to load config file. (Does not exists because of virtual environment)
  2. Ansible ping is not an ICMP ping, but a small module which requires a valid python env on host address.
  3. Ansible tries to establish a ssh connection which also requires keys. To ping localhost the command `--connection=local` has to be used.

- Ping to remote-server:

  `$ ansible all -i "2001:638:408:200:ff38::1," -m ping`

  Result:

    Remote server is unreachable because ssh connection is denied.


  ```bash
  2001:638:408:200:ff38::1 | UNREACHABLE! => {
      "changed": false,
      "msg": "Failed to connect to the host via ssh: thomas@2001:638:408:200:ff38::1: Permission denied (publickey,password).",
      "unreachable": true
  }
  ```

### c) Ping via hosts.yml

`$ ansible vm -i hosts.yml -m ping`


### d) Settings up development environment

Create a ansible configuration file:
`$ ansible-config init --disabled > ansible.cfg`

- Unncomment `remote_user`, add `tjonas2s`. Automatic remote_user resolution when connection to a remote host via ssh
- Uncomment `hosts`, add `hosts.yml`. Remove implicit listing of hosts filepath

### e) Getting current remote user name

By settings the verbose settings to `-vvv` the debug log prints the current user.

### f) Connect as root

`$ ansible vm -i hosts.yml --ask-become-pass -m ping` - Tries to connect as root. Requires manual password entry.


## Task 2 - Ansible-Role: Connection-Check

Create new role `conn-check` to ping a host:

`$ mkdir roles`

`$ cd roles`

`$ ansible-galaxy init conn-check`

Add task:

Inside `roles/conn-check/tasks/main.yml`:

```yml
- name: Test ping
  action: ping
```

Create playbook-file `pb-remoteserver-1.yml:

```yml
- name: ping remote server vm
  hosts: vm
  roles:
    - conn-check
```

Run role inside playbook:

`$ ansible-playbook pb-remoteserver-1.yml`


## Task 3 - Ansible-Role: Basics

Create a role `basics` to configure a server.
e.g. (harden SSH, change color of prompt based on user, install additional packages, configure vim)

Role which updates apt-package manager.
```yml
- name: Install packages
  ansible.builtin.apt:
    update_cache: yes
```

Related Playbook
```yml
- name: Update apt-packgage on remote server vm
  hosts: vm
  roles:
    - basics
  become: yes
```

Run role inside playbook (with sudo password asking):

`$ ansible-playbook pb-remoteserver-1.yml -K`


## Task 4 Ansible-Role: Docker-CE

- Used resource for installation via ansible: https://www.digitalocean.com/community/tutorials/how-to-use-ansible-to-install-and-set-up-docker-on-ubuntu-20-04

- Docker Version:         `Docker version 20.10.21, build baeda1f`
- Docker-Compose Version: `docker-compose version 1.29.2, build unknown`

## Task 5 Further Questions

- Diskutieren Sie die Verwendung von Sudo-Passworten bezüglich Notwendigkeit, Praktikabilität und Sicherheit beim Provisioning mit Ansible.

Password should not be stored in plain text. Especially not pushed inside public version controll systems.

- Überlegen Sie sich ein gutes Konzept, wie das Sudo-Passwort verschlüsselt in Ansible zur Verfügung gestellt werden kann. Erläutern Sie Ihr Konzept.

  - Create password inside ansible/temporary directory
  - Safe passwords in vault