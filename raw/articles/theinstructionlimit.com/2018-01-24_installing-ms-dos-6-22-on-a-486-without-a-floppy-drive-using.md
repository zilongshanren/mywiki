---
title: Installing MS-DOS 6.22 on a 486 without a floppy drive using a CF-to-IDE adapter
url: https://theinstructionlimit.com/installing-ms-dos-6-22-on-a-486-without-a-floppy-drive-using-a-cf-to-ide-adapter
author: Author Renaud Bédard
published: '2018-01-24'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

*A guide for a very specific problem, but hey, I had trouble doing it and pieced out the solution from a bunch of sources and advice, so here’s a distillation of that.*

![](../../assets/bb723eef3a26ccde.jpg)


I’m currently building a 486 “retro” PC for fun, out of parts sourced from a combination of my dad having it lying around in the basement, eBay, and generous friends.

My endgoal is to reproduce the PC setup I had as a kid; MS-DOS 6.22, [QuickBasic](https://en.wikipedia.org/wiki/QuickBASIC) 4.5, a bunch of DOS games and [ANSI art](https://en.wikipedia.org/wiki/ANSI_art) demos.

This week I was at point where I had everything to get started : a motherboard and CPU, graphics card, IDE hard drive, power supply, and a [Compact Flash to IDE adapter](https://www.google.ca/search?q=Compact+Flash+to+IDE+adapter&tbm=isch) with a 2Gb CF card.

I did not, however, have a floppy disk drive nor a CD-ROM drive. And it turns out installing MS-DOS without a FDD can be a tricky thing!

The options I saw just Googling variations of “*install ms-dos to usb*” (since on the modern PC, the CF card is connected via USB) were as follows :

- Use
[Rufus](https://rufus.akeo.ie/)to make a boot USB device : that only works if you want[FreeDOS](http://www.freedos.org/)(and it does work great for that), because Rufus is unable to make a MS-DOS 6 boot disk,[as acknowledged by its author](https://superuser.com/a/1228198). - Use
[UNetBootin](https://unetbootin.github.io/)or[dd](http://www.chrysocome.net/dd)or some other image burner to transfer a bootable disk image from[AllBootDisks](http://www.allbootdisks.com/download/iso.html)to USB : this probably does work, but not with CF-to-IDE adapters in my experience. Possibly because the disk/MBR layout of a fixed drive and a floppy must differ…? In any case, I was never able to make a bootable partition that way.

At this point I feel like I need to stress : this is not a sensible project. I could install FreeDOS or even Windows 98’s MS-DOS 7.0 relatively easily, but I don’t want to. There is no good reason.

Regardless, here’s the solution I ended up with. The whole thing assumes that the “modern PC” you’re setting all of that from is running Windows.

Here’s the gist : **use a virtual machine to mount the CF card as a virtual hard drive, then use the real MS-DOS 6.22 installer diskettes to create a partition and install DOS on it.**

In detailed steps :

- Grab the install disks for MS-DOS 6.22 (
[The Legacy PC Project](http://www.thelegacypcproject.com/software.html)hosts it currently) - Install
[VirtualBox](https://www.virtualbox.org/wiki/Downloads)for Windows hosts - Plug in your Compact Flash card (I have a 2Gb card, I’ve been told bigger than 2Gb can be problematic)
- Open a Command Prompt with Administrator rights (required for unmounting)
- Type the following to get the list of physical disks in your system.

This allows you to know what the DeviceID of your Compact Flash card is (should look like*\\.\PHYSICALDRIVE1*)wmic diskdrive list brief

- Find the drive letter associated with your CF card (through the Explorer), and unmount it by typing the following. (replace
*DRIVELETTER*by your drive letter)

This allows VirtualBox to have raw access to the drive.mountvol DRIVELETTER: /p

- Change directory to the folder where VirtualBox is installed (most likely
*C:\Program Files\Oracle\VirtualBox*) - Type the following to create a raw virtual machine disk (.vmdk) that maps to the whole device of the CF card.

(replace the*N*in*\\.\PhysicalDriveN*with the DeviceID you found earlier)vboxmanage internalcommands createrawvmdk -filename CompactFlashCard.vmdk -rawdisk \\.\PhysicalDriveN

- Start VirtualBox with Administrator rights (required for raw disk access)
- Create a DOS Virtual Machine (it’s under the “Other” type, Version is “DOS”), with default settings, except that when prompted about the hard disk, choose the “Use an existing virtual disk file” option and provide the
*CompactFlashCard.vmdk*file created earlier - Go in Settings for this VM, “Storage” section, click on the “Empty” first floppy drive and click on the diskette icon, and select “Choose Virtual Floppy Disk File…”. Then, browse to the first disk of the MS-DOS 6.22 install set.

![](../../assets/19c9487f51825d16.png)

- Start the VM, boot from floppy, and go through the installer.
- When prompted to switch to the next disk, you can choose it from the “Devices”, “Floppy Drive”, “Choose disk image…” menu item.

![](../../assets/85a519a445bae736.png)


There should be nothing special in the MS-DOS setup process itself at this point, just make sure you allocated a DOS partition in the hard drive you’ve mounted and set it as active… and you’re done!

You’ll have to use Disk Management to eject the device for your CF card (which is safer than just yanking it), but you don’t really need to assign a letter unless you want to browse its files directly from Windows.

Hi,

I tried, and almost succeeded !

My “only” problem is to make the CF card to be seen as actually bootable : when I restart without the DOS virtual floppy, it says that there’s no bootable medium found and that the system is halted…

Even if DOS is indeed installed on the CF card !

Can’t we make a disk image from virtual PC and clone it to the CF card later?

DOS on my 22-years old laptop, and it works well. Now I can play GORILLA.BAS every time I want.

Two details.

1. My CF is 4GB large. DOS installer simply use the firsts 2GB. So if you already have a CF larger than 2GB (and your hardware support this) you can using it without buy a specific CF.

2. In order to boot MS-DOS correctly (if doesn’t do) you have to zero erase your CF, like dd if=/dev/zero of=/dev/{CARD} bs=512 count=1 (on linux). It’s important: on my CF there was a quite modern OS and MS-DOS installer had some trouble to format the MBR.

This is a wondeful distillation of a scatttered topic confounding retro loving PC geeks everywhere.

however my own problem is: when MSDOS blue screen page 1 of setup asks to continue setup , to autoconfigure (format) the disk by pressing Y, it stops and gives me a general “error” while configuring my 512mb (ridata) CF card – yes, it was successfully unmounted too and i followed all the steps! it seems a LOT of trial and error with small CF cards is necessary. 1

The problem I ran into in both Mac OS and in Windows is as you described, the reason was that for some reason when swapping virtual floppy disks in the virtual drive, the host operating system remounts the CF or SD card, effectively leaving it inaccessible to the guest OS. I have not yet found a way around this.

I used this guide to set up DOS 6.22 on a Toshiba Laptop that doe snot have a Floppy Drive. I used the original 2GB IDE Drive for now. I had issues with the partition from the previous OS. I ended using DISKPART in windows 10 to clean the drive and then created the VMDK. That solved my FDISK problem and I formated the drive. DOS setup went great. After the drive was moved back to the real PC Windows 3.11 also installed without a hitch.

I had the same problem, I used windows 10 disk management to remove the disc in windows 10, the start with the setup as described here.

I’m trying to replicate the steps here, but MS-DOS installation keeps failing when formatting the the CF card: the format fo drive C is incompatible with MS-DOS 6.22

format c: reports “Unable to write BOOT”

I have zeroed the CF on Linux, but didn’t help.

Any ideas? Thanks a lot in advance

I have the same issue.. did you get yours working?

Hi guys,

I have resolved my issue for boot from CF with the command fdisk /mbr from the first floppy of MS-DOS 6.22

I was having trouble with the dos installer being unable to partition the disk. I discovered that you can delete the partition in windows 10’s disk management leaving the whole thing unpartitioned and then it worked fine. You can also assign or unassign drive letters and it will also tell you what physical drive it is. Dunno when any of these features were put in, but they’re definitely in 10.

I found a potentially simpler solution for people having trouble getting VirtualBox to successfully install DOS directly on to their CF/SD card. My SD card would fail whether it was DOS or FreeDOS, so I did some experimenting.

– Create a virtual drive with the same specs as your SD/CF card. (I don’t think the size actually matters, but just in case)

– Install DOS on to the virtual drive via VirtualBox and the DOS floppy images.

– Open powershell/cmd and navigate to the VirtualBox install directory

– Run .\vboxmanage internalcommands converttoraw ‘C:\PATH\TO\YOUR\VIRTUALDRIVE.vdi’ NameOfImage.img

– Plug in your CF/SD card.

– Open Rufus (https://rufus.ie/)

– Select your CF/SD card, set it to use a DD image, and browse to find the image you created above.

This should write the image of your virtual drive directly to the SD/CF card so that you can avoid the trouble of trying to directly tie a virtual drive to it.

This worked for me. The method in the post did not work. In fact, after issuing the /p, the drive was unmounted but also failed to show up at all until I used the Win10 Manage feature.

This guide worked well for me when following James additional procedure: delete partition in Windows 10, followed by letting Dos create it in Virtual Box. (Before that I got an error message in DOS about the disk being to small).

Most CF cards are not fully “IDE” compatible. i.e do not function within the operating system as a standard IDE disk would. The best option to succeed with a CF IDE adapter combination is to use an Industrial CF card that is 512MB to 2GB in size. This avoids problems with BIOS limitations and boot sectors not being correctly written. The majority of industrial cards perform better and do not have a removable bit set within them, as the consumer variants do which are for use within camera, mp3 players etc.. Most boot issues can be fixed using a few DOS commands, such as FDISK.EXE /mbr and SYS.EXE A: C: (A: being a bootable DOS disk and C: the formatted C: Disk). It is also important that the card is used in CHS mode and not LBA mode (google if you don’t know what these mean) as most 386/486 machines have a BIOS limitation of 2GB disk size and will not work or boot a LBA configured disk. Hope this helps some as I have great experience using CF disks in classic machines and industrial cards are more reliable.

I did a similar install on a thin client using usb but building the install in vm. Worked without a hitch. This is a good guide, it seams like the best way to do this in a post floppy age.

Virtual machine looks like overkill to be honest. I solved the same problem with RPMrepUSB, there’s an option for MS-DOS io.sys bootable drive, mandatory options are “Boot as HDD” and “Use 64hd/32sec”, then just extract MS-DOS iso file and select that path as a source for files

Excellent guide – thanks!

I tried it with a 4GB CF card from Transcend and the only additonal step(s) I had to do were…

-since fdisk denied to work with the attached card I had to create the partitions with “minitools partition wizard”

-after that I had to use fdisk again and it worked fine

So one extra step might be to “init” the cf card with an external tool.

Thanks a lot again as this enables me to save a lot of time installing the wanted setup on real hardware. After I have created such an image I store a backup with “hddrawcopy tool” and just transfer this image anew when something goes bonkers on the old PCs – disk corruption due to unstable hardware being one of the nastiest errors.

Hello, I tried this way, MS-DOS installed and working on Virtual Machine.

Next I’m turning machine off and plug CF card in old PC -> I’m getting “Missing operating system”. So I tried connect CF card again to my PC and assign drive letter to browse it. I’m little bit confused – in windows explorer I can see only DOS directory and wina20.386 file, without AUTOEXEC etc… Also, virtual machine is still working. My notebook can read CF card, becouse FreeDOS is working correctly. Have You maby any idea what can I doing wrong?

Best Regards!

Hi,

What kind of motherboard is it?

Do you have more details about the hardware, including the power supply?

Many Thanks

PS: cool page here.

Great post!

On my 286 system, the IDE HDD wouldn’t boot.

I did end up getting a 3.5 floppy to install DOS, it still wouldn’t boot off C:\, so had to use a boot floppy disk.

Typing FDISK /MBR from A:\ fixed this though and now the system boots off C:.