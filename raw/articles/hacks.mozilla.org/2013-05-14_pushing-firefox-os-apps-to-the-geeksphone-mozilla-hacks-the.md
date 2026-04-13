---
title: Pushing Firefox OS Apps to the Geeksphone – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/05/pushing-firefox-os-apps-to-the-geeksphone/
author: Posted
published: '2013-05-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A push to device feature was added in the 3.0 release of the [Firefox OS Simulator](https://hacks.mozilla.org/2013/05/firefox-os-simulator-3-0-released/). This feature allows web apps to be pushed to a connected device by clicking one button in the Simulator Dashboard. Availability of the [Developer Preview Phone from Geeksphone](https://hacks.mozilla.org/2013/04/geeksphone-to-start-selling-firefox-os-developer-preview-phones/) has raised interest in the feature, so this post will detail how to configure your Geeksphone and the computer running the Simulator to make use of it.

![Firefox OS Simulator on a Mac](../../assets/8f7109d76de182d8.png)


## Setting Up the Geeksphone Device

To push apps to the Geeksphone Firefox OS Developer Preview phone, you first need to enable Remote debugging. This can be done from the Settings app by selecting Device information > More Information > Developer -> Remote debugging. Now we are ready to configure the computer running the Simulator.

### Windows

The team at Geeksphone recently released a set of drivers for Windows to support USB communication with their phones. The [drivers are available at Geeksphone’s Web Site (direct ZIP link)](http://downloads.geeksphone.com/drivers/usb_driver.zip).

To install them, first download and extract the zip file to a known location on your system. Next, connect the phone to your machine using the provided USB cable. Click on the Start Button and enter “Device Manager” in the Search programs and files text entry field and press enter. This will launch the Windows Device Manager. Alternatively, you can launch the Device Manager from the icon located in the Windows Control Panel.

![Device Manager before driver installed](../../assets/92ddbde2c2f2c58e.png)


The connected phone will be listed under the Other Devices category. Right click on the Android label and select Update Driver Software….

![Right Click options](../../assets/b40943ac87cc7038.png)


In the Update Driver Software dialog, choose Browse my computer for driver software.

![Update driver dialog](../../assets/17ea95edab279a07.png)


Locate the usb_driver folder from the Geeksphone download and make sure the Include subfolders checkbox is checked. Click on the Next button.

![Locate Driver](../../assets/e493b1bd5659bc05.png)


You will most likely receive a Windows Security alert. Select the Install this driver software anyway entry.

![Windows security alert prompt](../../assets/6f0459e96c04a41d.png)


This will install the proper USB drivers and list the phone as Geeksphone Device in the Device Manager.

![Device manager with drivers updated](../../assets/215624f931954a8b.png)


Launch the Firefox OS Simulator. The Dashboard should now contain a Push button and a Device connected message, and you should be able to add your Firefox OS app to the Simulator and push it to the phone.

### Linux

If you are running the Simulator on a Linux machine, you will need to create or modify a udev rules file for the device. This process is described in “[Setting up a Device for Development](https://developer.android.com/tools/device.html)” (Steps 3.a and 3.b). The Geeksphone Firefox OS Developer Preview phone idVendor attribute is “05c6”, so your android.rules file should contain an entry similar to:

```
SUBSYSTEM==”usb”, ATTR{idVendor}==”05c6”, MODE=”0666”, GROUP=”plugdev”
```

After making the above changes, either reboot the system or restart the udev service:

```
sudo service udev restart
```

If you make these changes and the push to device button does not show up in the Simulator Dashboard, please see this [workaround](https://github.com/mozilla/r2d2b2g/issues/515).

### Mac

If you are running the Simulator on a Mac, no additional configuration is required to enable push to device.

## Reference

Additional information about setting up and using the Firefox OS Simulator, including installing, adding apps, debugging and using the push to device capability can be found on the MDN page for the [Firefox OS Simulator](https://developer.mozilla.org/en-US/docs/Tools/Firefox_OS_Simulator).

## 8 comments

Antoine TurmelMay 14th, 2013 at 16:36Robert Nyman [Editor]May 14th, 2013 at 23:11ArasMay 20th, 2013 at 23:36Jason WeathersbyMay 21st, 2013 at 14:28ArasMay 21st, 2013 at 22:08ArasMay 22nd, 2013 at 02:16Jason WeathersbyMay 22nd, 2013 at 13:51Julie SullivanMay 22nd, 2013 at 14:04