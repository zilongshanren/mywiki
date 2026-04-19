---
title: BTRFS, Quick Start
url: https://www.4rknova.com/blog/2018/10/27/btrfs
author: Nikolaos Papadopoulos
published: '2018-10-27'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Introduction

I finally got a chance to look into RAID and after a bit of research decided to give BTRFS a try. BTRFS has some issues, which are documented [here](https://btrfs.wiki.kernel.org/index.php/Status) but for the setup that I am interested in, it appears to be mostly stable. This guide documents the steps I followed to setup my system.

# Hardware / System

For this build, I am using 2x Western Digital (3.5”) Red 4TB hard drives, in a RAID1 configuration and the host machine is running Debian Sid. The Linux kernel version at the time of writting this guide was 4.7.0-1-amd64.

# BTRFS RAID1

The following paragraph is copied verbatim from the official BTRFS FAQ page.

[…] BTRFS combines all the devices into a storage pool first, and then duplicates the chunks as file data is created. RAID-1 is defined as “2 copies of all the data on different devices”. This differs from MD-RAID and DMRAID, in that those make exactly n copies for n devices. In a btrfs RAID-1 on three 1 TB devices we get 1.5 TB of usable data. Because each block is only copied to 2 devices, writing a given block only requires exactly 2 devices to be written to; reading can be made from only one […]


BTRFS RAID1 allows for a single drive redundancy; if more than one disk fails at the same time, there is high probability of losing data.

# Setting up a new array

The first step is to install the btrfs utilities.

$ sudo apt-get install btrfs-tools

Next the disks need to be formatted. In this example x is the 1st device and y is the 2nd device. Replace the letters accordingly to match your configuration.

$ sudo mkfs.btrfs -m raid1 -d raid1 /dev/sdx /dev/sdy

Check if the system recognizes the array

$ sudo btrfs fi show Label: 'disk1' uuid: 5b732a75-4490-852a-3447-a47c8af59aa3 Total devices 2 FS bytes used 128.00KiB devid 1 size 3.64TiB used 2.01GiB path /dev/sdx devid 2 size 3.64TiB used 2.01GiB path /dev/sdy

Optionally, you can add a label to your array:

$ sudo btrfs filesystem label /dev/sdx data

Finally add the following entry to your /etc/fstab. Replace the UUID below with the uuid of one of the drives in the array:

UUID=5b732a75-4490-852a-3447-a47c8af59aa3 /media/data btrfs defaults 0 0

# Adding auxiliary devices

It’s possible to add more devices to an existing array. First, check the existing BTRFS filesystems and which devices they include.

$ sudo btrfs filesystem show

Add the new device to the array. Notice that the mount point is used to identify the array.

$ sudo btrfs device add /dev/sdz /media/data/

At this point we have a filesystem with three drives, but all of the metadata and data are still stored on the original two drives. The filesystem must be balanced to spread the extents across all the drives. Please note that this operation takes a long time and might require leaving it running overnight. To balance (restripe) the allocated extents across all of the existing devices use the following command:

$ sudo btrfs filesystem balance /media/data

You’ll get an output similar to below:

WARNING: Full balance without filters requested. This operation is very intense and takes potentially very long. It is recommended to use the balance filters to narrow down the scope of balance. Use 'btrfs balance start --full-balance' option to skip this warning. The operation will start in 10 seconds. Use Ctrl-C to stop it. 10 9 8 7 6 5 4 3 2 1 Starting balance without any filters. Done, had to relocate 3352 out of 3352 chunks

# Disk Space Usage

If RAID is active, it will be visible in the btrfs filesystem df command. The output is hard to read at first as the tool reports the amount of space allocated per type of data rather then an occupancy percentage with regards to the total capacity of the array.

$ btrfs fi df /media/data Data, RAID1: total=2.92TB, used=2.91TB System, RAID1: total=33.55MB, used=425.98kB Metadata, RAID1: total=4.29GB, used=2.94GB GlobalReserve, single: total=536.87MB, used=0.00B

Also, the values shown by df are not reliable, as it is hard to predict how disk usage will behave in a copy-on-write and snapshotting filesystem like btrfs.

Running regular df we can observe a few interesting things:

df -h Filesystem Size Used Avail Use% Mounted on /dev/sdx 7.3T 2.7T 4.7T 37% /media/data

The total size of the array is 7.3TB but BTRFS has reserved 2.92TB for data and 4.29GB for metadata. This roughly correlates with the values reported in regular df, as the used space amounts to 2.7TB. In general the amount of space BRTFS reserves for each type of data depends on how balanced the filesystem is. If you run into space related issues, running a balance is probably the best way to go.

# Maintenance

As with every storage media, it’s always a good idea to regularly check the health of the hardware to make sure that faulty hardware is replaced in time and no data is lost.

## BTRFS Tools

BTRFS provides a stats command, which keeps track of errors (including read, write and corruption/checksum errors) per drive.

$ sudo btrfs device stats /media/data/

This command will yield an output similar to the following:

[/dev/sdx].write_io_errs 0 [/dev/sdx].read_io_errs 0 [/dev/sdx].flush_io_errs 0 [/dev/sdx].corruption_errs 0 [/dev/sdx].generation_errs 0 [/dev/sdy].write_io_errs 0 [/dev/sdy].read_io_errs 0 [/dev/sdy].flush_io_errs 0 [/dev/sdy].corruption_errs 0 [/dev/sdy].generation_errs 0

A simple root cronjob could be used to report errors:

sudo crontab -e

Add the following entry, after replacing the path:

@daily btrfs device stats /media/data | grep -vE ' 0$'

This will check for positive error counts every day and send a message to your local mailbox if any issues arise.

It’s also recommended to schedule a scrub every month to detect silent corruption caused by a bad drive. The scrub process will read all data and metadata blocks from all devices, verify checksums and automatically repair corrupted blocks if there’s a correct copy available.

@monthly btrfs scrub start -Bq /media/data

## S.M.A.R.T.

For all drives that are attached to the RAID array you can schedule a long S.M.A.R.T. test. The following command will initiate the test.

smartctl --test=long /dev/sdx

To get the result of the S.M.A.R.T test when that is complete, use the following command.

smartctl -A -H /dev/sdx

It’s important to note that S.M.A.R.T. tests put a strain on the drive and it would best to not schedule them to automatically happen on a frequent basis.