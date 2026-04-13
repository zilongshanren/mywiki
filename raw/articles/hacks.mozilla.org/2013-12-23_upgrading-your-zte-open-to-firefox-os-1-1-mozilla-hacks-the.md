---
title: Upgrading your ZTE Open to Firefox OS 1.1 – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/12/upgrading-your-zte-open-to-firefox-os-1-1/
author: Frédéric Harper
published: '2013-12-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![ZTE Open](../../assets/9e827e828b0ab104.jpg)


The US and the European versions of the ZTE Open both ship with version 1.0 of Firefox OS. Since an over the air (OTA) update is not yet available for the phone, ZTE recently posted a build and instructions on how to flash the phone with Firefox OS 1.1, the latest released version of the OS, on their website. Let’s see how to do it. (Note: the procedure requires a microSD card to store the build before you flash it on your phone.)

## Download the Firmware

Depending on the version of the phone you purchased, you need either the US or the UK (European) version of the firmware. Download the files from the ZTE support site by clicking the “Downloads” tab on one of these pages: [US version](http://www.ztedevices.com/support/smart_phone/b5a2981a-1714-4ac7-89e1-630e93e220f8.html) or [UK version](http://www.ztedevices.com/support/smart_phone/cba40ed6-d3ab-44c0-bdee-3a15803dc187.html). The zip file you’ll download will also contain documentation for the upgrade.

## Prepare Your Phone

The upgrade process will erase all user data such as contacts. At present, there is no operating system feature for backing up contacts, but if you need to retain them, try installing and running the [Con Backup app](https://marketplace.firefox.com/app/contacts-backup/) in the Firefox Marketplace to back your contacts up to your microSD card.

When you are ready, follow these steps to prepare your phone:

- Charge your phone to at least the 50% level to insure there is plenty of power to complete the upgrade process.
- Extract the contents from the zip file you downloaded. At the top level, there should be a PDF file with instructions for the upgrade and another zip file with the firmware. The instructions are essentially the same as those given in this post.
- Power off your phone, remove the battery to access the microSD card and extract the card from its holder.
- Connect the microSD card to your desktop machine.
- Move US_DEV_FFOS_V1.1.0B04_UNFUS_SD.zip or EU_DEV_FFOS_V1.1.0B04_UNFUS_SD.zip (depending on the version you downloaded) to the root directory of your microSD card. Do not unzip the file.
- Disconnect the microSD card from your desktop computer and return it to your phone.

![Firefox OS Recovery Mode](../../assets/b0304f2a93119a78.jpg)


## Upgrade to 1.1

Follow these steps:

- Press the volume up and the power key simultaneously. Volume up is activated by pressing the upper part of the long key on the left side of the phone. If you did it properly, you’ll enter the Firefox OS recovery mode. (Note that the Firefox OS logo may display briefly before you enter the recovery mode.)
- Use the volume up/down key to move from one item to the other in the menu, and chose “apply update from external storage.”
- Press the power key to confirm the selection. You’ll see a new screen listing the files you have on the microSD card.
- Again use volume up/down key to select the firmware: either US_DEV_FFOS_V1.1.0B04_UNFUS_SD.zip or EU_DEV_FFOS_V1.1.0B04_UNFUS_SD.zip (depending on the version you downloaded), and press the power key to confirm.

![Install from sdcard complete](../../assets/25e7bcfb552a3b5c.jpg)


If everything went well, you’ll see a sequence of status messages, culminating with one that says, “Install from sdcard complete.” You’ll need to select “reboot system now”: your phone will reboot, and you’ll see the configuration screen you saw the first time you powered on the phone.

After the process completes, you can remove the firmware zip file from your microSD card to reclaim the space. If somehow you bricked your phone–which shouldn’t happen if you had a sufficient charge on the battery and followed these steps–use [this documentation](https://developer.mozilla.org/en-US/Firefox_OS/Developer_phone_guide/ZTE_OPEN#I_bricked_my_phone) to recover.

Congratulations, your phone is now running with Firefox OS 1.1! You will now benefit from all the bug fixes, [new features for users](http://www.mozilla.org/en-US/firefox/os/notes/1.1/) and [new features for developers](https://developer.mozilla.org/en-US/Firefox_OS/Releases/1.1) of the latest released build of Firefox OS.

## About
[
Frédéric Harper ](http://outofcomfortzone.net)

As a Senior Technical Evangelist at Mozilla, Fred shares his passion about the Open Web, and help developers be successful with Firefox OS. Experienced speaker, t-shirts wearer, long-time blogger, passionate hugger, and HTML5 lover, Fred lives in Montréal, and speak Frenglish. Always conscious about the importance of unicorns, and gnomes, you can read about these topics, and other thoughts at outofcomfortzone.net.

## About
[
Mark Coggins ](http://cogswells.tumblr.com/)

Mark is the former SVP of Engineering at Actuate, a public company in the Business Intelligence space. He is co-founder of the BIRT open source project at the Eclipse Foundation, and is the author of six crime novels set in the Silicon Valley.

## 64 comments

Emanuel HoogeveenDecember 23rd, 2013 at 09:52Frédéric HarperJanuary 6th, 2014 at 08:35Mister_WJanuary 20th, 2014 at 14:21Mister_WJanuary 20th, 2014 at 14:24Frédéric HarperJanuary 31st, 2014 at 08:18elavDecember 23rd, 2013 at 10:17Mark CogginsDecember 23rd, 2013 at 11:22Adam HarveyDecember 23rd, 2013 at 13:45Mark CogginsDecember 23rd, 2013 at 18:08Adam HarveyDecember 23rd, 2013 at 18:21Bob ThulframDecember 23rd, 2013 at 17:10Mark CogginsDecember 23rd, 2013 at 18:07M. Edward Borasky (@znmeb)December 23rd, 2013 at 21:25Bob ThulframDecember 23rd, 2013 at 23:14M. Edward Borasky (@znmeb)December 23rd, 2013 at 23:22Frédéric HarperJanuary 6th, 2014 at 08:38Steve EllisDecember 23rd, 2013 at 17:15Mark CogginsDecember 23rd, 2013 at 18:03Frédéric HarperJanuary 6th, 2014 at 08:39aquilaxDecember 23rd, 2013 at 20:36Frédéric HarperJanuary 6th, 2014 at 08:41Jürgen PetryDecember 24th, 2013 at 10:13Mark CogginsDecember 24th, 2013 at 10:16Jürgen PetryDecember 24th, 2013 at 10:39Jürgen PetryDecember 24th, 2013 at 14:32Richard KillingsworthDecember 24th, 2013 at 11:28David RichardsonDecember 30th, 2013 at 15:43Richard KillingsworthJanuary 1st, 2014 at 04:15ᙇᓐ M. Edward Borasky (@znmeb)January 17th, 2014 at 12:15Richard KillingsworthJanuary 1st, 2014 at 04:21Frédéric HarperJanuary 31st, 2014 at 08:21JonhDecember 25th, 2013 at 03:21Frédéric HarperJanuary 6th, 2014 at 08:46AndrewDecember 25th, 2013 at 16:31Frédéric HarperJanuary 6th, 2014 at 08:47Laurens DebackereJanuary 6th, 2014 at 11:23Maire ReavyJanuary 10th, 2014 at 12:34Maire ReavyJanuary 10th, 2014 at 12:40ᙇᓐ M. Edward Borasky (@znmeb)January 10th, 2014 at 13:23Sean SilvaJanuary 12th, 2014 at 14:14Mark CogginsJanuary 12th, 2014 at 16:34Patrick H. LaukeJanuary 14th, 2014 at 01:34Mister_WJanuary 15th, 2014 at 08:12ᙇᓐ M. Edward Borasky (@znmeb)January 15th, 2014 at 12:43Mister_WJanuary 15th, 2014 at 12:50ᙇᓐ M. Edward Borasky (@znmeb)January 15th, 2014 at 14:51Frédéric HarperJanuary 31st, 2014 at 08:23Mister_WJanuary 15th, 2014 at 15:04Bob ThulframJanuary 15th, 2014 at 19:08ᙇᓐ M. Edward Borasky (@znmeb)January 17th, 2014 at 12:13Mister_WJanuary 16th, 2014 at 06:02ᙇᓐ M. Edward Borasky (@znmeb)January 16th, 2014 at 12:22AbhiramJanuary 17th, 2014 at 13:06ᙇᓐ M. Edward Borasky (@znmeb)January 17th, 2014 at 13:28Jeff JohnsonJanuary 17th, 2014 at 11:56Frédéric HarperJanuary 20th, 2014 at 12:09NinoJanuary 19th, 2014 at 07:37Richard KillingsworthJanuary 21st, 2014 at 01:37Gerry FerdinandusJanuary 20th, 2014 at 14:41Gerry FerdinandusJanuary 20th, 2014 at 16:53Paul HanningtonJanuary 22nd, 2014 at 06:39Paul HanningtonJanuary 22nd, 2014 at 07:44Jude AJanuary 21st, 2014 at 12:34Mark CogginsJanuary 21st, 2014 at 15:48