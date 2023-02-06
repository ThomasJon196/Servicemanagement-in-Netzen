## Aufgabe 1 - Installation von Ubuntu 22.04 auf der VM

Install Ubuntu 22.04 on VM

- Einfügen der gewuenschten ubuntu.iso in das virtuelle CD Laufwerk
- Server hochfahren.
- Betriebssystem über die console installieren.

## Aufgabe 2

a. Configure an IPv6 interface for the VM with the provided IPv6 address.

> Added a new global IPv6 address and gateway to the netplan configuration.


b. Interpret the Configuration-File:

`/etc/netplan/00-installer-config.yaml`
```yaml
network:
  ethernets:
    ens19:
      dhcp4: true
    ens18:
      addresses:
        - 2001:638:408:200:FE28::1/64 # Adresse
      routes:
        - to: default
          via: 2001:638:408:200::1    # Gateway
  version: 2
```


## Aufgabe 3

a. Use OpenSSH to establish a ssh connection with the VM.

> Create a local RSA-keypair via `ssh-keygen`.
> Add the public-key to `~/.ssh/authorized_keys` inside the VM

- Zugriff ueber ssh: `ssh tjonas2s@2001:638:408:200:FE28::1`

b. How to disable password authentication?

- Passwort-Zugriff ausschalten: `PasswordAuthentication no`


## Aufgabe 4

- ping kommt an
