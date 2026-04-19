---
title: ZEXMTE BT-506 in Debian
url: https://www.4rknova.com/blog/2023/04/22/zexmte-bluetooth-debian
author: Nikolaos Papadopoulos
published: '2023-04-22'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

I recently purchased a ZEXMTE BT-506 bluetooth dongle from [amazon](https://www.amazon.co.uk/dp/B09NVPTS6J) to use in a Debian Linux server.

# Installation

This dongle uses a Realtek RTL8761B chipset. A quick check using apt suggests that the required firmware is included in the *firmware-realtek* package.

% apt show firmware-realtek | grep RTL8761B * Realtek RTL8761B Bluetooth config (rtl_bt/rtl8761b_config.bin) * Realtek RTL8761B Bluetooth firmware (rtl_bt/rtl8761b_fw.bin) * Realtek RTL8761BU Bluetooth config (rtl_bt/rtl8761bu_config.bin) * Realtek RTL8761BU Bluetooth firmware (rtl_bt/rtl8761bu_fw.bin)

Unfortunately after installation, the system was still failing to load the firmware. A quick inspection of */lib/firmware/rtl_bt* also confirmed that the relevant files were missing. The solution was to copy the files manually. I used [the linux kernel archives](https://git.kernel.org) as a source.

$ cd /lib/firmware/rtl_bt $ sudo wget https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/rtl_bt/rtl8761bu_config.bin $ sudo wget https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/rtl_bt/rtl8761bu_fw.bin

# Power management issues

While using the device, I’ve noticed that it occasionally becomes unresponsive after an unspecified time of operation. Some quick online research reveals that this issue is associated with USB autosuspension. My understanding is that this is a common issue due to the majority of vendors not implementing support for this feature correctly.

One workaround, if the Linux kernel is compiled with usbcore embedded, is to set the *usbcore.autosuspend* option to *-1*. This works for Debian and Ubuntu.

If the Grub bootloader is used, modify the “GRUB_CMDLINE_LINUX_DEFAULT” entry in */etc/default/grub* to add that option.

```
GRUB_CMDLINE_LINUX_DEFAULT="quiet usbcore.autosuspend=-1"
```


Then update grub.

$ sudo update-grub`

After a reboot, the configuration can easily be verified.

$ cat /sys/module/usbcore/parameters/autosuspend -1