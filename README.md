# mbpi-garage-opener
Project to integrate two Micro:Bits and a Raspberry Pi to manage the open/close state of a garage door as well as opening and closing.

## Wireguard Install On Raspian Buster

This section of the project is aimed at using a mobile phone to create a vpn connection to the Raspberry Pi. This allows the end user to connect to the app on the Pi to see the status of the garage door and either open or close it.
___

Commands performed on a fresh install of Raspberry Pi OS (32-bit) Lite (formerly Raspbian) for the Raspberry Pi

https://www.raspberrypi.org/downloads/raspberry-pi-os/

OS Details for current install:
Minimal image based on Debian Buster
Version: May 2020
Release date: 2020-05-27
Kernel version: 4.19
Size: 432 MB

## Raspberry Pi (Server) setup
Install Debian's public keys since Raspberry Pi OS doesn't trust Debian's package repo:  
`sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 04EE7237B7D453EC 648ACFD622F3D138`

Add package repos to the sources list:  
`sudo sh -c "echo 'deb http://deb.debian.org/debian/ unstable main' >> /etc/apt/sources.list.d/unstable.list"`

```bash
sudo sh -c "printf 'Package: *\nPin: release a=unstable\nPin-Priority: 90\n' >> /etc/apt/preferences.d/limit-unstable"
```

Update to download the latest packages from these repos:
`sudo apt update`

Install Wireguard:
`sudo apt install wireguard --assume-yes`

Install QR Encode for adding transferring public, private, and server settings to phone.
`sudo apt install qrencode`

To avoid the 'RTNETLINK answers: Operation not supported' error install the kernel headers, dkms, and tools packages.
`sudo apt install raspberrypi-kernel-headers wireguard-dkms wireguard-tools`

Add an interface named wg0:
`ip link add dev wg0 type wireguard`

Add the IP addressing for connecting peers:
`ip address add dev wg0 10.200.200.1/24`

Create public/private keys for the Raspberry Pi server, laptop, and two mobile phones
```bash
wg genkey | tee wg-pi-server-private.key | wg pubkey > wg-pi-server-public.key

wg genkey | tee wg-laptop-private.key |  wg pubkey > wg-laptop-public.key

wg genkey | tee wg-mobile1-private.key | wg pubkey > wg-mobile1-public.key

wg genkey | tee wg-mobile2-private.key | wg pubkey > wg-mobile2-public.key
```
Create the configuration file
`sudo nano /etc/wireguard/wg0.conf`

Add the following to /etc/wireguard/wg0.conf
```bash
[Interface]
Address = 10.200.200.1/24
ListenPort = 51820
PrivateKey = <copy private key from wg-server-private.key>
PostUp   = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o wlan -j MASQUERADE
ListenPort = 51820

[Peer]
# laptop
PublicKey = < wg-laptop-public.key >
AllowedIPs = 10.200.200.2/32

[Peer]
# mobile phone1
PublicKey = <wg-mobile1-public.key>
AllowedIPs = 10.200.200.3/32

[Peer]
# mobile phone2
PublicKey = <wg-mobile2-public.key>
AllowedIPs = 10.200.200.4/32
```

Setup internal forwarding on the Pi to allowing access to other machines/devices on your network
`sysctl net.ipv4.ip_forward=1`

Make IP forwarding persistent:
`sudo nano /etc/sysctl.conf`
then uncomment:
\#net.ipv4.ip_forward=1

Start the wireguard service:
`sudo wg-quick up wg0`

Set the wireguard service to start boot
`sudo systemctl enable wg-quick@wg0.service`

### Client mobile phone setup
A config needs to be added for each device that had a set of public/private keys created.

In the same directory that the public/private keys create a conf file for each device. In this case mobile1.conf & mobile2.conf

In the same directory where you have the public/private keys saved run:
`sudo nano mobile1.conf`

Then paste the following config into mobile1.conf:
```bash
[Interface]
Address = 10.200.200.3/24
PrivateKey = <copy private key from wg-mobile-private.key>
DNS = 10.200.200.1
        
[Peer]
PublicKey = <copy public key from wg-server-public.key>
AllowedIPs = 0.0.0.0/0
Endpoint = <public ip or ddns address>:51820
```

To safely transfer the keys for mobile1.conf to your mobile phone a qr code can be created within the terminal.

Run the following command to create the QR code from the mobile1.conf settings:
`qrencode -t ansiutf8 < mobile.conf`

This will generate a QR within the linux terminal.

### Phone setup :iphone:
1. Download and install the WireGuard app on your phone.
2. Click the + button to create a vpn tunnel
3. Select the Scan From QR Code option
4. Once the camera opens point it to the QR code in the Linux terminal to have all the settings from mobile1.conf transferred to the phone

### Laptop Setup :computer:
Out of the scope but might be added later down the road
