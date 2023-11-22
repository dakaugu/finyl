## Pre Setup
Create a github token with `admin:public_key`, `read:org, repo` and add it the drive. <br>
### Create a file for wifi connectivity in your Pi device
Create a file called `50-cloud-init.yaml` and add the content below with your wifi SSID and password. <br>
and add it to th drive
```
# This file is generated from information provided by the datasource.  Changes
# to it will not persist across an instance reboot.  To disable cloud-init's
# network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
    ethernets:
        eth0:
            dhcp4: true
            optional: true
    version: 2
    wifis:
        wlp3s0:
            optional: true
            access-points:
                "SSID-NAME-HERE":
                    password: "PASSWORD-HERE"
            dhcp4: true
```
Boot up a Raspberry Pi with the drive. Get your drive's name and mount it. <br>
```shell
sudo lsblk
```
Mount it, after identifying the name <br>
```shell
sudo mkdir /media/usb_drive && mount /dev/sdb /media/usb_drive
```
Replace `sdb` with your device name. <br>
Copy your network file into your raspberry pi:
```shell
sudo cp -f /media/usb_drive/50-cloud-init.yaml /etc/netplan/50-cloud-init.yaml
```
Apply the changes:
```shell
sudo netplan apply
```
If all went well you would be able to see your wireless adapter connected to the wireless network by executing the `ip` command:
```shell
ip a
```
### Configure github
Install github cli:
```shell
sudo apt install gh
```
Authenticate against github by reading the token from a file
```shell
gh auth login --with-token < /media/usb_drivee/gh_token.txt
```
You can now clone Finyl and run the installation.sh script
