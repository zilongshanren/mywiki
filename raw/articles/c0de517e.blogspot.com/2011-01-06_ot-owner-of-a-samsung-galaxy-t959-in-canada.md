---
title: 'OT: Owner of a Samsung Galaxy T959? In Canada?'
url: http://c0de517e.blogspot.com/2011/01/ot-owner-of-samsung-galaxy-t959-in.html
published: '2011-01-06'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Off topic, but it took me a bit to figure everything out and I hate, I hate, I hate having to tinker with technology (I love that I can, but I hate that I have to) so I'll post some tips if you, like me, did a cheap contract with Wind or Mobilicity, hated their phones and took the bad decision of buying an android based samsung galaxy from the US instead (only the US T-Mobile T959 will work with these carriers in canada).

The T959 officially only has Android 2.1 that sucks, so I've also ventured into the realms of firmware updating. Anyways, this is the to-do list.

1) Visit the xda-developers forums, they have all the info:

[http://forum.xda-developers.com/wiki/index.php?title=Samsung_Galaxy_S_SGH-T959](http://forum.xda-developers.com/wiki/index.php?title=Samsung_Galaxy_S_SGH-T959)2) Root the phone (easiest way is to connect it to wifi and download this app: http://forum.xda-developers.com/showthread.php?t=746129 then reboot the phone into recovery mode and select "install packages").

3) Remove the carrier lock, it's not too hard. You'll need to download the android drivers, connect it with the USB cable and use ADB, that's a command-line android shell, let's you log into the phone from the PC. It involves doing some trickery with nv_data and generating some keys with a program, it will take a few commands (

[http://forum.xda-developers.com/showthread.php?t=822008&highlight=unlock](http://forum.xda-developers.com/showthread.php?t=822008&highlight=unlock))4) Download the ROM Manager application and flash a good rom. I've found the team whiskey ones (

The modem is very important to have a decent data reception, it also affects battery use and GPS. You can even flash different modems on top of an existing firmware but I guess it's better to have a firmware that already includes the latest modem.

Note that you might need to reboot into recovery and use the "install packages" option twice in order to have the rom manager recovery menu installed in the phone... Note also that the firmware .zip has to be moved into the "internal sd" can't stay into the external (transflash) storage.

About "lagfixes": these appear to be hacks that let older kernels to use ext4 (I think) filesystem, thus making the phone quicker and removing lags. I'm not enabling these, if you do beware that if you flash a firmware that does not support these lagfixes the phone will not boot, as it won't recognize the FS. A flash with Odin, with the phone in download mode will be necessary then.


5) Condition your battery. Fully charge it and then let it fully discharge a few times, the phone will "record" the power levels and optimize the indicator. It's also advised to flash the new rom with the battery fully charged, otherwise the battery indicator will be wrong until you recondition.

[http://www.teamwhiskey.com/DownVibrant.html](http://www.teamwhiskey.com/DownVibrant.html)) to be the best so far, it's a clean rom (no weird themes, no shit) and it's updated with the latest firmware and latest 2.2 modem (JL5). Update: Now the 2.2 is official from samsung. Still you can download the teamwhiskey version that comes with all sorts of tunings and most importantly the "voodoo" improvements (ext4, better display and audio) built in.The modem is very important to have a decent data reception, it also affects battery use and GPS. You can even flash different modems on top of an existing firmware but I guess it's better to have a firmware that already includes the latest modem.

Note that you might need to reboot into recovery and use the "install packages" option twice in order to have the rom manager recovery menu installed in the phone... Note also that the firmware .zip has to be moved into the "internal sd" can't stay into the external (transflash) storage.

About "lagfixes": these appear to be hacks that let older kernels to use ext4 (I think) filesystem, thus making the phone quicker and removing lags. I'm not enabling these, if you do beware that if you flash a firmware that does not support these lagfixes the phone will not boot, as it won't recognize the FS. A flash with Odin, with the phone in download mode will be necessary then.

5) Condition your battery. Fully charge it and then let it fully discharge a few times, the phone will "record" the power levels and optimize the indicator. It's also advised to flash the new rom with the battery fully charged, otherwise the battery indicator will be wrong until you recondition.

6) If you screw up don't panic, chances are that you can still put your phone into download mode and use Odin to flash the stock samsung rom. Normally the ROM Manager is way better to flash stuff, use Odin only if the phone does not work anymore.

7) See this to set the phone parameters to work with Wind. Note that it might work even without touching the service mode settings, even it it might be convenient to lock it to the 1700 and 2100 bands only if you want to avoid roaming and have the phone lock on the "wind home" faster:


8) Fix your GPS. Better software settings here:

[http://forum.xda-developers.com/showthread.php?p=10241844](http://forum.xda-developers.com/showthread.php?p=10241844)8) Fix your GPS. Better software settings here:

## 3 comments:

You had me up until step 7! Why on earth would a bad rooting or carrier experience make you want to go to an iphone? iphone is limited to AT&T in the USA and their speeds and coverage is horrible.

If you are in the usa then the post does not apply, as per its title. I dunno about phones in the us at all. Still all other things being equal i have to say i'd prefer an ios phone aver an abdroid one, much less hassle, much more robust.

An additional fix for the galaxy s (vibrant... i9000...). http://forum.xda-developers.com/showthread.php?t=784691 - removes all those, sometime second long, hitches the phone shows.


Cheers!

Post a Comment