---
title: Upgrading your ZTE Open to Firefox 1.1 or 1.2 (fastboot enabled) – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/01/upgrading-your-zte-open-to-firefox-1-1-or-1-2-fastboot-enabled/
author: Frédéric Harper
published: '2014-01-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![FoxLove](../../assets/a743fa78a174c660.jpg)


If you are a ZTE Open owner, you may have already upgraded to Firefox OS 1.1 [following the instructions from our previous post](https://hacks.mozilla.org/2013/12/upgrading-your-zte-open-to-firefox-os-1-1/). If so, you probably realized that the latest build from ZTE had a problem: fastboot wasn’t enabled anymore. For those of you who didn’t upgrade because of that, ZTE has put a new build of 1.1 with fastboot enabled on their site.

Depending on the version of the phone you purchased, you need either the US or the UK (European) version of the build. Download the files from the ZTE support site by clicking the “Downloads” tab on one of these pages: [US version](http://www.ztedevices.com/support/smart_phone/b5a2981a-1714-4ac7-89e1-630e93e220f8.html) or [UK version](http://www.ztedevices.com/support/smart_phone/cba40ed6-d3ab-44c0-bdee-3a15803dc187.html). The zip file you’ll download will also contain documentation for the upgrade, or you can follow [our earlier instructions](https://hacks.mozilla.org/2013/12/upgrading-your-zte-open-to-firefox-os-1-1/).

## Upgrading to Firefox 1.2

We are pleased to announce that ZTE has also made available a version of Firefox OS 1.2. If you want to upgrade to it, you’ll first need to install the version of 1.1 that has fastboot enabled (or be on an older version of the OS with fastboot enabled). Next, you need to verify that you can establish a connection with the phone via USB. This [post](https://hacks.mozilla.org/2013/08/pushing-a-firefox-os-web-app-to-zte-open-phone/) describes how to configure Windows, Linux and Mac machines for a USB connection (something you’ll want to do anyway if you are pushing apps to your phone during development).

Finally, you’ll need to have have fastboot from the [Android Developer Toolkit](http://developer.android.com/sdk/index.html) installed on your desktop machine. It is not necessary to install the entire toolkit. adb and fastboot are found in the /platform-tools/ folder. They can be copied to /usr/bin of your Linux or Mac OS X machine, or copied to another folder as long as that folder is added to your $PATH.

After your phone and your desktop computer are properly configured, connect your phone to your computer via USB cable and try to restart your device with this command from the console (in Windows, open a command prompt window):

`fastboot reboot`

If your phone reboots itself, you are good to go for the upgrade. Download the appropriate version of the build from the Dropbox account ZTE has set up: [US version](https://www.dropbox.com/sh/rnj3rja7gd54s98/32KXfFmedN/P752D04_DEV_US_20131212_v1.2.7z) or [UK version](https://www.dropbox.com/sh/rnj3rja7gd54s98/_twgXEkMFH/P752D04_DEV_EU_20131212_v1.2.7z). For Windows users, you can also [download special instructions](https://www.dropbox.com/sh/rnj3rja7gd54s98/6ZoJwmlRjn/Installation%20Instruction.docx), and [an upgrade tool](https://www.dropbox.com/sh/rnj3rja7gd54s98/-fyi2XHFPG/upgrade_tool) to help you to install the new version easily. In this post, however, I provide steps for **all operating systems**–Linux, OS X, and Windows–without relying on the special tool.

Once you have the file, extract the contents, and open a console. Note that those steps will erase your personal data, so be sure to make a backup first. Then navigate to the folder where the files are. Still in the console, type this command:

```
adb reboot bootloader
```

Wait for your phone to reboot, and while it is rebooting, execute those commands:

```
fastboot flash boot boot.img
fastboot flash userdata userdata.img
fastboot flash system system.img
fastboot flash recovery recovery.img
fastboot erase cache
fastboot reboot
```

![ZTE Open upgraded to Firefox OS 1.2](../../assets/233cfb53a305f043.png)

The software version you see after upgrading

If everything went well, your phone should reboot at this point. You’ll find that this version of 1.2 from ZTE includes many test applications, which you can remove if you like.

Congratulations, your phone is now running Firefox OS 1.2! You will benefit from all the bug fixes, [new features for users](http://www.mozilla.org/en-US/firefox/os/notes/1.2/), and [new features for developers](https://developer.mozilla.org/en-US/Firefox_OS/Releases/1.2) of the latest released build of Firefox OS.

*If you have any questions related to the upgrade, I invite you to submit them on our StackOverflow Q&A. You’ll benefit from the expertise of thousands of people, including our Technical Evangelist team.*

## 2014-02-05 Updates

We updated the process as some users had booting issues after upgrading to 1.2. Some users also reported us being able to execute the command, even if the fastboot test (fastboot restart) wasn’t working: I can’t confirm, but please try, and let us know if it’s working.

## About
[
Frédéric Harper ](http://outofcomfortzone.net)

As a Senior Technical Evangelist at Mozilla, Fred shares his passion about the Open Web, and help developers be successful with Firefox OS. Experienced speaker, t-shirts wearer, long-time blogger, passionate hugger, and HTML5 lover, Fred lives in Montréal, and speak Frenglish. Always conscious about the importance of unicorns, and gnomes, you can read about these topics, and other thoughts at outofcomfortzone.net.

## 124 comments

Sourav LahotiJanuary 30th, 2014 at 10:47Frédéric HarperJanuary 30th, 2014 at 11:29Gregorio EspadasJanuary 30th, 2014 at 11:26Frédéric HarperJanuary 30th, 2014 at 11:30marekJanuary 30th, 2014 at 14:34Frédéric HarperJanuary 31st, 2014 at 07:42elavJanuary 30th, 2014 at 11:46Frédéric HarperJanuary 30th, 2014 at 12:08elavJanuary 30th, 2014 at 12:17Frédéric HarperJanuary 30th, 2014 at 12:36elavJanuary 31st, 2014 at 13:19elavJanuary 31st, 2014 at 13:41LukeJanuary 30th, 2014 at 20:26Frédéric HarperJanuary 31st, 2014 at 07:46Frédéric HarperFebruary 5th, 2014 at 11:34Daniel BriertonJanuary 30th, 2014 at 11:59Frédéric HarperJanuary 30th, 2014 at 12:02Daniel BriertonJanuary 30th, 2014 at 12:01Frédéric HarperJanuary 30th, 2014 at 12:03K EveretsJanuary 30th, 2014 at 13:32Frédéric HarperJanuary 30th, 2014 at 13:34K EveretsJanuary 30th, 2014 at 13:37K EveretsJanuary 30th, 2014 at 13:35Frédéric HarperJanuary 31st, 2014 at 08:13KonFebruary 1st, 2014 at 17:09Frédéric HarperFebruary 5th, 2014 at 11:36asdf3February 13th, 2014 at 21:59Jeff JohnsonFebruary 1st, 2014 at 19:37Akmal IrfanFebruary 2nd, 2014 at 17:00Frédéric HarperFebruary 5th, 2014 at 11:39Jeff JohnsonFebruary 7th, 2014 at 12:45KonFebruary 3rd, 2014 at 14:57Frédéric HarperFebruary 5th, 2014 at 11:42K EveretsFebruary 5th, 2014 at 13:58Frédéric HarperFebruary 5th, 2014 at 14:06K EveretsFebruary 5th, 2014 at 14:10Juan EladioJanuary 30th, 2014 at 18:20Frédéric HarperJanuary 31st, 2014 at 07:49kaieJanuary 30th, 2014 at 18:26Frédéric HarperJanuary 31st, 2014 at 08:14Milan JosipovicJanuary 30th, 2014 at 20:36al3xaJanuary 30th, 2014 at 21:25Frédéric HarperJanuary 31st, 2014 at 07:52tuxorJanuary 31st, 2014 at 15:59Mister_WJanuary 31st, 2014 at 09:02Luca F.February 1st, 2014 at 11:05jotaassFebruary 1st, 2014 at 12:30Nghi TranFebruary 1st, 2014 at 22:35Akmal IrfanFebruary 2nd, 2014 at 16:56Frédéric HarperFebruary 5th, 2014 at 11:56TolokobanFebruary 5th, 2014 at 12:47Frédéric HarperFebruary 5th, 2014 at 14:08Michael NiemannJanuary 31st, 2014 at 13:28Frédéric HarperJanuary 31st, 2014 at 13:30Michael NiemannJanuary 31st, 2014 at 14:34Frédéric HarperFebruary 5th, 2014 at 12:01DonJJanuary 31st, 2014 at 17:49DonJJanuary 31st, 2014 at 17:52donzJanuary 31st, 2014 at 18:03Gerry FerdinandusFebruary 1st, 2014 at 20:24RolandFebruary 2nd, 2014 at 05:15jezraFebruary 5th, 2014 at 11:55Frédéric HarperFebruary 5th, 2014 at 12:03Frédéric HarperFebruary 5th, 2014 at 13:35TolokobanFebruary 2nd, 2014 at 12:17TolokobanFebruary 2nd, 2014 at 14:04Frédéric HarperFebruary 5th, 2014 at 12:18TolokobanFebruary 5th, 2014 at 12:40ArasFebruary 2nd, 2014 at 18:59Frédéric HarperFebruary 5th, 2014 at 12:22RolandFebruary 3rd, 2014 at 02:50Frédéric HarperFebruary 5th, 2014 at 12:23ThePeachFebruary 3rd, 2014 at 08:49Frédéric HarperFebruary 5th, 2014 at 12:24ThePeachFebruary 5th, 2014 at 12:33Benjamin KerensaFebruary 3rd, 2014 at 18:37Frédéric HarperFebruary 5th, 2014 at 14:10jezraFebruary 5th, 2014 at 12:03Frédéric HarperFebruary 5th, 2014 at 13:36Frédéric HarperFebruary 5th, 2014 at 14:03LukeFebruary 5th, 2014 at 23:49Mister_WFebruary 6th, 2014 at 03:22PaviFebruary 6th, 2014 at 06:05elavFebruary 6th, 2014 at 07:14Frédéric HarperFebruary 6th, 2014 at 08:30elavFebruary 6th, 2014 at 09:25Maurizio RTOSkitFebruary 7th, 2014 at 13:53elavFebruary 10th, 2014 at 06:50IvanFebruary 6th, 2014 at 13:49PraveenFebruary 7th, 2014 at 01:409825February 7th, 2014 at 02:38IvanFebruary 7th, 2014 at 05:26naugturFebruary 23rd, 2014 at 14:06Jack GuoFebruary 7th, 2014 at 22:36EtemFebruary 10th, 2014 at 03:37Akmal IrfanFebruary 11th, 2014 at 05:28Jeff JohnsonFebruary 11th, 2014 at 09:19Félim WhiteleyFebruary 11th, 2014 at 16:58>8[February 13th, 2014 at 01:48Jeff JohnsonFebruary 13th, 2014 at 12:27asdfsaFebruary 14th, 2014 at 00:11kazhikFebruary 14th, 2014 at 14:37Jeff JohnsonFebruary 18th, 2014 at 07:30EvertonFebruary 16th, 2014 at 17:53Frédéric HarperFebruary 17th, 2014 at 09:02ReeceFebruary 17th, 2014 at 14:37Frédéric HarperFebruary 18th, 2014 at 09:13ReeceFebruary 18th, 2014 at 14:13Vladimir SinotovFebruary 21st, 2014 at 06:21Eric ShepherdFebruary 23rd, 2014 at 15:25PaviFebruary 23rd, 2014 at 17:41ReeceFebruary 24th, 2014 at 09:39PhiloPolyMathFebruary 24th, 2014 at 23:10ReeceFebruary 25th, 2014 at 03:09PhiloPolyMathFebruary 25th, 2014 at 06:46GerryFebruary 25th, 2014 at 16:25PhiloPolyMathFebruary 26th, 2014 at 08:04GerryFebruary 26th, 2014 at 15:24PhiloPolyMathFebruary 26th, 2014 at 15:36PhiloPolyMathFebruary 26th, 2014 at 18:32PhiloPolyMathFebruary 26th, 2014 at 20:37ReeceFebruary 25th, 2014 at 07:14ChadFebruary 26th, 2014 at 00:11PhiloPolyMathFebruary 27th, 2014 at 12:07