---
title: Pushing a Firefox OS Web App to ZTE Open phone – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/08/pushing-a-firefox-os-web-app-to-zte-open-phone/
author: Posted
published: '2013-08-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

ZTE recently announced release of the [ZTE Open Firefox OS phone](https://fxosphone.mozilla.com.tw/zteopen/), a device aimed at developers and early adopters. In this post we cover the basic details of connecting and configuring your desktop environment to push Apps to the ZTE Open from the Firefox OS Simulator.

## Setting Up the ZTE Open

Before pushing or debugging an App on the ZTE Open you must first enable remote debugging on the phone. This can be done by selecting Device information->More Information->Developer->Remote debugging within the Settings Application.

![remote debug setting](../../assets/a3d7e31b6a7bcac2.png)


## Windows

To connect the Simulator to the ZTE Open on Windows platforms requires a specific USB driver. ZTE has made available a self-contained executable that will install the proper driver. This executable can be found on the ZTE site.

[OPEN(American Standard – phones purchased from e-Bay US store)](http://www.ztedevices.com/support/smart_phone/b5a2981a-1714-4ac7-89e1-630e93e220f8.html)

[OPEN(European Standard – phones purchased from e-Bay UK store)](http://www.ztedevices.com/support/smart_phone/cba40ed6-d3ab-44c0-bdee-3a15803dc187.html)

Choose the proper link and select downloads. The driver will be labeled DRV_PKG_ZTE_VERSION.

To install these drivers, first download and extract the Zip file to a known location on your Windows system. Next connect the phone to your machine using the provided USB cable. Run the “ZTE_Handset_USB_Driver.exe” executable within the extracted zip file.

![Windows Folder Browser](../../assets/c6966a9f15481008.png)


Step through the setup wizard to install the driver.

![ZTE Setup Wizard](../../assets/1489d3400f383e89.png)


Once you have installed the driver, you should be able to push an App to the device. You can verify that driver is installed by checking the device manager. The ZTE phone will be listed under Android Phone as ZTE Kernel Debug Interface.

![Windows Device Manager](../../assets/bd7f847d5b63cc23.png)


Launch the Firefox OS Simulator and the Dashboard should now contain a Push button and a Device connected message.

![Simulator Dashboard](../../assets/1a6ba6270a59efa7.png)


You should now be able to add your Firefox OS App to the Simulator and then Push it to the phone.

## Linux

If you are developing on a Linux platform, you need to add a udev rule to allow a connection to be made to the ZTE Open. Complete steps 3.a and 3.b listed under [“Setting up a Device for Development”](https://developer.android.com/tools/device.html) within the Android documentation. The ZTE Open uses “19d2” as the idVendor attribute. The rule should look similar to the following:

```
SUBSYSTEM==”usb”, ATTR{idVendor}==”19d2”, MODE=”0666”, GROUP=”plugdev”
```

After making the above changes, either reboot the system or restart the udev service:

```
sudo service udev restart
```

If the push to device button does not show up in the Simulator Dashboard please see this [bug](https://github.com/mozilla/r2d2b2g/issues/515).

## Mac

If you are running the Simulator on a Mac, no additional configuration is required to enable push to device.

## Reference

For general information on using the Simulator to push and debug an App, make sure to take a look at the [“Firefox OS Simulator”](https://developer.mozilla.org/en-US/docs/Tools/Firefox_OS_Simulator) documentation.

## 17 comments

christianAugust 29th, 2013 at 19:09RanandarAugust 30th, 2013 at 06:19Jason WeathersbyAugust 30th, 2013 at 13:34Robert SaylesSeptember 2nd, 2013 at 21:26Andre Alves GarziaSeptember 1st, 2013 at 09:46Mathew PorterAugust 30th, 2013 at 02:44Alex GrenierAugust 30th, 2013 at 07:41MumpiHAugust 30th, 2013 at 10:13chrisAugust 31st, 2013 at 01:18Chris HeilmannAugust 31st, 2013 at 15:14ChrisAugust 31st, 2013 at 19:35Chris HeilmannSeptember 1st, 2013 at 07:48IT Support LondonSeptember 2nd, 2013 at 02:09JuriSeptember 6th, 2013 at 00:25Jason WeathersbySeptember 6th, 2013 at 12:20JuriSeptember 9th, 2013 at 10:55Kataskeui Istoselidon ThessalonikiSeptember 21st, 2013 at 07:29