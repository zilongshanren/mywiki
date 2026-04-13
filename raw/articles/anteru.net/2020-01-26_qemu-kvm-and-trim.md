---
title: QEMU, KVM and trim
url: https://anteru.net/blog/2020/qemu-kvm-and-trim
published: '2020-01-26'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I’m using [KVM](https://www.linux-kvm.org/) for (nearly) all my virtualization needs, and over time, disk images get bigger and bigger. That’s quite annoying if you know that a lot of the disk space is unused, and it’s only due to blocks not getting freed in the guest OS and thus remaining non-zero on the host. All modern file systems have a notion of sparse files which don’t require any physical memory to store zeroes. On top of that, any modern OS supports the [ TRIM](https://en.wikipedia.org/wiki/TRIM) command to notify the hardware that a block can be de-allocated, but if you’re using KVM with

[and the default settings, then you’ll not get any of those benefits. High time we fix this!](https://virt-manager.org/)

`virt-manager`

This guide works for both Windows and Linux; the setup is the same, but triggering `TRIM`

from the OS is different. First of all, you’ll want to switch the drives from `VirtIO`

to `SCSI`

and use the `VirtIO`

SCSI adapter (which supports `TRIM`

since quite some time, while the `blk`

driver only recently learned about it). That’s relatively simple to do in the UI, after you stopped your virtual machine:

- Open your disk
- Goto “Advanced options”, change the bus to “SCSI”, apply. This generates a new controller “Controller SCSI 0”. We’ll get to the controller in a second. Before that, open up “Performance options” and select
`unmap`

for “Discard mode” and (optionally) “Detect zeroes” (for details, check the)`libvirt`

documentation - Now, click on the controller which was just created and change the model to “VirtIO SCSI”

You can also modify the XML directly, in this case, for the disk, you’ll want:

```
<disk>
<driver name='qemu' type='qcow2' discard='unmap' detect_zeroes='unmap'>
<target dev='...' bus='scsi'>
</disk>
```


and for the controller:

```
<controller type='scsi' model='virtio-scsi'>
<address>
</controller>
```


For Windows, make sure that *before* you do the switch, you install the [“VirtIO” vioscsi drivers](https://docs.fedoraproject.org/en-US/quick-docs/creating-windows-virtual-machines-using-virtio-drivers/index.html). Otherwise, Windows will refuse to boot. For Linux, I didn’t have to change anything (tried with Ubuntu 18.04 and CentOS 8 as guests).

After you boot into your OS, you’ll want to manually toggle a trim.

- For Windows, run
`Optimize-Volume -DriveLetter C -ReTrim -Verbose`

in an elevated command prompt - For Linux, run
`fstrim -a -v`

with root privileges

This should only take a few seconds and report the trimmed space. You can check immediately on your host using `du -h *`

if the operation was successful. In my case, it reduced the size of my Windows VM from 50 GiB to 26 GiB – a significant saving when doing backups, as all those zeroes can be skipped *very* quickly. Happy virtualization!