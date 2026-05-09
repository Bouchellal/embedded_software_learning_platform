# Raspberry Pi SD card programming

<details>
<summary><strong>How to flash the Raspberry Pi OS onto an SD card (first time or maintenance)</strong></summary>

- Take an SD card of a minimum size of 8 GB.
- Download the latest Raspberry Pi Imager from the [Raspberry Pi website](https://www.raspberrypi.com/software/).
- Follow the following screenshots to flash the Raspberry Pi OS onto the SD card using the Raspberry Pi Imager:

![Raspberry Pi Imager](../.images/99_platform/rpi_img_1.PNG)
![Raspberry Pi Imager](../.images/99_platform/rpi_img_2.PNG)
![Raspberry Pi Imager](../.images/99_platform/rpi_img_3.PNG)
![Raspberry Pi Imager](../.images/99_platform/rpi_img_4.PNG)
![Raspberry Pi Imager](../.images/99_platform/rpi_img_5.PNG)
![Raspberry Pi Imager](../.images/99_platform/rpi_img_6.PNG)
![Raspberry Pi Imager](../.images/99_platform/rpi_img_7.PNG)
![Raspberry Pi Imager](../.images/99_platform/rpi_img_8.PNG)
![Raspberry Pi Imager](../.images/99_platform/rpi_img_9.PNG)
![Raspberry Pi Imager](../.images/99_platform/rpi_img_10.PNG)

- Insert the SD card into a **LINUX PC** or other device capable of reading ext4 file systems.
- Open the rootfs partition:

![Raspberry Pi SD Card](../.images/99_platform/sd_card_rootfs_1.PNG)

- Open a terminal at this level:

![Raspberry Pi SD Card](../.images/99_platform/sd_card_rootfs_2.PNG)

- Run the following command from the terminal:

```bash
etc/NetworkManager/system-connections/eth0.nmconnection
```

- Copy the following content into the file:

```yaml
[connection]
id=eth0-static
type=ethernet
interface-name=eth0

[ethernet]

[ipv4]
method=manual
addresses=192.168.1.100/24
gateway=192.168.1.1
dns=1.1.1.1;8.8.8.8;

[ipv6]
method=disabled
```

- Run the following command to grant the necessary permissions to the file:

```bash
chmod 600 /etc/NetworkManager/system-connections/eth0.nmconnection
```

- Eject the SD card and insert it into the Raspberry Pi.
- Power on the Raspberry Pi and wait for it to boot up.
- Test the connection by following the [Hands On Guide](../02_hands_on_platform/README.md).

</details>
