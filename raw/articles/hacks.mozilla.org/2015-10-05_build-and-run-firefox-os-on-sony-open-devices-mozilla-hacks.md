---
title: Build and Run Firefox OS on Sony Open Devices – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/10/build-and-run-firefox-os-on-sony-open-devices/
author: Dietrich Ayala; Alexandre Lissy Posted; Mobile
published: '2015-10-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A few years ago, Sony released their first port of Firefox OS, for the Xperia E. Since then, [Sony has started the Open Devices initiative](http://developer.sonymobile.com/knowledge-base/open-source/open-devices/) to bring support for AOSP (the Android Open Source Project) to many more of its smartphones. The porting work described in this post is based on this effort and brings Firefox OS to a dozen different Sony devices.

![Sony tablet and phone](../../assets/d2c1d9b7ddeff815.jpg)


## Build from the FXP Project

Builds of Firefox OS for a number of Sony devices are now available from the [FXP project](http://fxpblog.co/firefox/nightly/). Thanks to Adam Farden for his work on improving the default look and feel of unbranded Firefox OS builds, and hosting these images. These builds also have over-the-air updates, so you can stay up to date as Firefox OS continues to improve! They’re built from the nightly branch of Firefox OS though, so make sure to back up your information regularly.

![FXP Project](../../assets/094f1a7b35a87e7a.png)


Read on to create your own build of Firefox OS for a Sony Xperia device…

## Building Firefox OS

Before you begin, a few warnings:

**TIME!**It will take*overnight*to download the source code. I am not joking! Expect it to take 10 hours or more to fetch the entire source tree. Firefox OS sits atop a number of other projects, including Linux, the Android Open Source Project, and many others. Building a smartphone image is not like building the Firefox browser, or even like compiling a custom kernel.**DATA!**Flashing your device will destroy the existing operating system and may delete your user data. Always do a complete back-up of any information you want to keep.**BRICKS!**Flashing a new operating system on a device always comes with the risk of rendering the device permanently unusable. It’s rare, but possible. Sony provides an official tool called[Emma](http://developer.sonymobile.com/services/flash-tool/how-to-download-and-install-the-flash-tool/). It works with the S1 Bootloader flashmode so the chances of completely destroying a device are indeed very low and mostly everything can be saved by this tool. It is very simple to use and[documentation](http://developer.sonymobile.com/services/flash-tool/use-the-flash-tool-for-xperia-devices/)is available. It’s running in Windows but we have been using it successfully in VirtualBox: don’t forget that the USB IDs for S1 Bootloader mode are different. So you need to force your device to be attached to the virtual machine.

Oh, you’re still here? Great, but don’t say we didn’t warn you. Read on to learn how to build Firefox OS for your Sony device!

## Device Support

Firefox OS currently has support for the Shinano and Yukon Sony device platforms. This means that you can build for the Xperia Z2, Z3, Z3 Compact, Z3 Tablet Compact, as well as the E3, T2 Ultra. Support for the Xperia M2 should be available soon. You can see the full list of devices that are supported on [Sony’s website](http://fxpblog.co/active/). Note that your device to be flashed must be updated to Android Lollipop (5.1) prior to flashing.

Most features of Firefox OS are tested and you can expect these to work. This includes phone, SMS/MMS, and data connections, as well as device capabilities such as Wi-Fi, GPS, Bluetooth, and NFC.

The only major exception to this is the camera. The Sony team is porting the camera, and we’ll update this post when they’ve completed that work. The FM radio is also not yet supported. Areas where you might see variable support or some bugs are in audio/video decoding and processing, and hardware acceleration. Make sure to report a bug if you see a problem in these areas. Instructions for reporting issues are at the bottom of this post.

## Getting Ready to Build

Mozilla’s developer site, MDN, has [extensive documentation on building Firefox OS](https://developer.mozilla.org/en-US/Firefox_OS/Building_and_installing_Firefox_OS) for devices. Currently the only supported operating systems for building Firefox OS are 64-bit Linux. Start by installing the prerequisites (things like Git and the Android SDK) and setting up your [build environment](https://developer.mozilla.org/en-US/Firefox_OS/Firefox_OS_build_prerequisites). Follow the directions there and you’ll be just fine.

## Clone, Configure, Build

Once you’ve the build environment taken care of, you’re ready to [get the source code](https://developer.mozilla.org/en-US/Firefox_OS/Preparing_for_your_first_B2G_build). Remember, this may take many many hours! The code comes from many different repositories, and can take 10 hours or more even over a fast internet connection. Make sure you have at least 20gb of free disk space available for the source code and the build files that you will be generating.

The next few steps look like this:

* Clone the root repository of the project, which downloads the build scripts. This takes about a minute over a decent connection.

* Configuring for your device, which downloads all the B2G and Gonk source code and some configuration files and libraries specific to your device. This can take 10 hours or more over a decent connection.

* Compiling into a device image which can be flashed to the device. This step should take about an hour on a decently powered desktop computer.

Start by cloning the B2G repository with the command below. This should only take a minute:

```
git clone git://github.com/mozilla-b2g/B2G.git
```


This will have created a B2G directory, which you can now enter:

```
cd B2G
```


Before you begin the next step, connect your device through USB, and confirm that you can see it connected by executing the following command:

```
adb devices
```


You should see something like:

```
List of devices attached
YT910VTPWY device
```


Next you’ll configure the build for your specific device, using its code name. You can find your device code name by executing the config.sh script with no arguments:

```
./config.sh
```


Once you’ve found it, you can now configure the build. Here’s the configure step for the Z3 Compact:

```
./config.sh aries-l
```


The immediate next step is to go sleep. Or drive to visit your grandmother. Or see if you can run a marathon before the source code finishes downloading.

Okay! It’s the next day, and you’ve got all the source code. You’re now ready to build:

```
./build.sh
```


Now go watch half of a movie, or see how many push-ups you can do in an hour!

## Flash Your Device

This is the moment you’ve been waiting for. Make sure your device is connected via USB and then execute the following command:

```
./flash.sh
```


You should see the device go into bootloader mode and then various files being copied over and then written to it:

![Terminal while flashing](../../assets/699a1d2b7467084f.png)


After the flashing process is complete, your device will reboot into Firefox OS!

![Boot screen](../../assets/dcab9d17d9b963ec.jpg)


## That looks great, how can I help?

There are several ways you can contribute and stay in touch. One of the most obvious is getting access to a device already supported, and using it and [reporting bugs](https://bugzilla.mozilla.org/enter_bug.cgi?product=Firefox%20OS&component=GonkIntegration). Another step forward is hacking the device to help maintain it, making sure bug are fixed, and providing a smooth user experience. For those of you who are brave enough, you can help bring support for more Sony Xperia devices. The list of devices supported by the [Open Devices](http://developer.sonymobile.com/knowledge-base/open-source/open-devices/list-of-devices-and-resources/) project is bigger than those currently working with Firefox OS. For example, hacking to get the Z1/Z1 Compact series (Rhine platform) would be a good start.

Got questions about running Firefox OS on new hardware or devices? Try the [dev-fxos mailing list](https://lists.mozilla.org/listinfo/dev-fxos) or #fxos on IRC. Thanks!

## 11 comments

NawfelOctober 5th, 2015 at 11:08dattazOctober 5th, 2015 at 21:40NawfelOctober 6th, 2015 at 02:32NawfelOctober 6th, 2015 at 02:48dattazOctober 6th, 2015 at 06:23sgalbiaOctober 9th, 2015 at 22:53Dietrich AyalaOctober 11th, 2015 at 15:09Vincent den BoerOctober 14th, 2015 at 10:33Dietrich AyalaOctober 14th, 2015 at 13:56niu techOctober 15th, 2015 at 07:45bac_a_sableNovember 4th, 2015 at 05:33