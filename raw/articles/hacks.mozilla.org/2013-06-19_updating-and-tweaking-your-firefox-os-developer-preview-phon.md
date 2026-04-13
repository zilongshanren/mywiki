---
title: Updating and Tweaking your Firefox OS Developer Preview phone/Geeksphone –
  Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/06/updating-and-tweaking-your-firefox-os-developer-preview-phonegeeksphone/
author: Robert Nyman; Frédéric Harper Posted
published: '2013-06-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Developer Preview editions of the Firefox OS phone are now becoming widely available to the community, mainly through [Geeksphone](http://www.geeksphone.com/). Since these are for developers, naturally we want to encourage you to tinker and play with them as much as possible!

In this post we will cover some basic tips on how to keep your phone up to date and how to tweak the system Gaia applications.

## Updating your Geeksphone to the latest images

Firefox OS updates can be be downloaded from within the Settings app, listed under Device information. The phone can be set to check for updates daily, weekly or monthly. In addition a “check now” button is provided. When an update is available you will be prompted to download and install the current version.

![](../../assets/ff3c00424c0ddd0b.png)


The team at Geeksphone is also now providing the latest stable and nightly builds as self contained downloads for flashing your phone. Before proceeding make you have setup your phone as described in “Setting Up the Geeksphone Device” section of the [Pushing Firefox OS Apps to the Geeksphone](https://hacks.mozilla.org/2013/05/pushing-firefox-os-apps-to-the-geeksphone/) post. This will insure that you can push data to the phone.

The builds are located at the [Geeksphone download site](http://downloads.geeksphone.com/). On this site you will be presented with options for selecting your device and what type of build you want to use.

Download your particular build and extract the archive to your filesystem. The archive contains the images and commands required to flash the phone using Windows, Mac OS X or Linux. Before attempting to flash the phone make sure that you have enabled Remote debugging on the phone. This option can be set by launching the Settings app and navigating to the `Device information -> More information -> Developer`

tab. Also do not attempt to flash the phone if the power level is below 50%.

![](../../assets/b68f97f238dd67e2.png)


### Windows

Open a Command Prompt (`start -> type cmd in search -> enter`

on windows 7, `Windows key + X -> select Command Prompt`

on Windows 8) and cd to the directory containing the extracted files. Run:

```
flash.bat
```

### Mac OS X

Open a Terminal (`Cmd + space -> type terminal -> enter`

) window and cd to the directory containing the extracted files. Run:

```
./flash_mac.sh
```

**Updated Nov 12th 2013**

There are some new steps you need to do before being able to run the command above:

- You need to download
[Android SDK](http://developer.android.com/sdk/index.html): it’s because you need tools like adb & flashboot. - Unzip the file, and move it to the application folder: optionally, you can rename the folder to something like AndroidSDK (I’ll use AndroidSDK in next steps).
- Open (or create if it didn’t exists)
`~/.bash_profile`

, and adds this line`export PATH=${PATH}:/Applications/AndroidSDK/sdk/platform-tools`

– change AndroidSDK to reflect the SDK folder name you used in step 2.

### Linux

Open a Terminal (control-alt-t on Ubuntu) window and cd to the directory containing the extracted files. Run:

```
./flash.sh
```

This should flash the new image to the phone. The phone will need to be setup again as all data will be cleared.

## If you have an ‘unagi’ or developer preview phone that is not a Geeksphone

If you have a developer phone that is not a geeksphone such as an ‘unagi’ or a previously Android-based device, you may need to perform the following steps. If this is not you, please skip to the next section.

You will need to install **adb** and **fastboot**. These utilities can be found in the Android Developer Toolkit.

It is not necessary to install the entire toolkit. Download a the toolkit from here, and extract the contents. adb and fastboot are found in the /platform-tools/ folder. They can be copied to the /usr/bin of you Linux or Mac OS X machine, or copied to another folder as long as that folder is added to your $PATH.

If you are attempting to flash your device and have another device plugged in via USB, your phone may not be detected by these utilities correctly. Only have your phone plugged in while trying to flash it.

## Tweaking Gaia

If you are of the industrious sort, you may want to tweak the default applications in Gaia – the UI in Firefox OS. In this section we will cover some of the basics for cloning Gaia and making changes to the default system apps. Bear in mind these tips are “at your own risk” and may involve you reading the later section “Ok, I bricked my phone”. Before proceeding make sure that you have adb and fastboot installed on your system. To verify if these are installed open a terminal and type adb devices with your phone connected. You should see you phone listed under the attached devices.

You should also be able to run fastboot from the terminal. If you run fastboot, a set of parameter options should be displayed. If you do not have adb or fastboot installed, a quick Google search with your operating system will return several quick starts on how to install them. In addition to adb and fastboot you will need Git. If you do not currently have Git installed have a look at this [setup guide](https://help.github.com/articles/set-up-git). Finally make sure your phone is setup for remote debugging as described in the previous section.

Once you have the prerequisites you can open a terminal and cd to the directory you would like to clone the Gaia source code to and type the following commands.

```
git clone git://github.com/mozilla-b2g/gaia.git gaia
cd gaia
```

This will clone the current Gaia code to your system. If you plan on submitting changes back to the Gaia source, be sure to fork the source before cloning as described in [Hacking Gaia](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/Platform/Gaia/Hacking). Currently the Geeksphone Keon uses the v1.0.1 branch of Gaia code, so set the proper branch using the following command.

```
git checkout -b v1.0.1 origin/v1.0.1
```

Most of the system apps are located in the apps subdirectory of gaia. You can now make any changes to these Firefox OS apps you wish. Once you have made changes run the following command to push the modified apps to your phone. This will by default push all the system apps to the phone:

```
B2G_SYSTEM_APPS=1 make install-gaia
```

If you only changed one of the apps you can specify the particular app using similar syntax. In this example only the calendar app will be pushed to the phone:

```
APP=calendar B2G_SYSTEM_APPS=1 make install-gaia
```

If you have issues while making the changes, you can reset the phone to default values using either of the following commands.

```
make production
make reset-gaia
```

Note: Bear in mind that either of the above commands will clear any data or apps that you have pushed to the phone.

## “Ok, I bricked my phone”

If you are in the process of modifying your phone and it becomes “unresponsive” you should be able to recover it using fastboot with a simple procedure. The following illustrates reseting the Keon but other phones should have a similar process. You will also need to verify that you have fastboot installed.

First remove the USB cable and then remove the battery from the phone for thirty seconds. Then reinsert the battery and press the volume down button while holding the power button for a few seconds. Next re-connect the usb cable and run the following commands from a terminal window in the directory that contains the latest img files described in the first section of this post.

```
fastboot flash recovery recovery.img
fastboot flash boot boot.img
fastboot flash userdata userdata.img
fastboot flash system system.img
fastboot reboot
```

This process should recover your phone.

## Go play!

We hope these instructions are useful to you, and naturally we want you to be as happy about Firefox OS and the possibilities as we are! Feel free to play around with updating your devices, making changes/updates to Gaia apps and also to be inspired to take these learnings into [building your own Open Web Apps](https://hacks.mozilla.org/2013/02/getting-started-with-open-web-apps-why-and-how/).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## About
[
Frédéric Harper ](http://outofcomfortzone.net)

As a Senior Technical Evangelist at Mozilla, Fred shares his passion about the Open Web, and help developers be successful with Firefox OS. Experienced speaker, t-shirts wearer, long-time blogger, passionate hugger, and HTML5 lover, Fred lives in Montréal, and speak Frenglish. Always conscious about the importance of unicorns, and gnomes, you can read about these topics, and other thoughts at outofcomfortzone.net.

## 31 comments

Nicolas HoizeyJune 19th, 2013 at 06:37ChristianJune 19th, 2013 at 07:52Jason WeathersbyJune 19th, 2013 at 08:02Nicolas HoizeyJune 19th, 2013 at 08:12Jason WeathersbyJune 19th, 2013 at 11:05ChristianJune 19th, 2013 at 06:42Jason WeathersbyJune 19th, 2013 at 08:04Will EastcottJune 19th, 2013 at 10:45Jason WeathersbyJune 19th, 2013 at 11:06Robert Nyman [Editor]June 19th, 2013 at 12:59Ankit BahugunaJune 19th, 2013 at 23:08Alexandre GirardJune 20th, 2013 at 08:04Jason WeathersbyJune 20th, 2013 at 13:38Jason WeathersbyJune 20th, 2013 at 13:41Alexandre GirardJune 20th, 2013 at 23:44Lucas Salton CardinaliJune 20th, 2013 at 16:42Robert Nyman [Editor]June 24th, 2013 at 10:01anptrJune 22nd, 2013 at 15:04Jason WeathersbyJune 24th, 2013 at 09:10Bob ThulframJune 23rd, 2013 at 00:45Robert Nyman [Editor]June 24th, 2013 at 10:02Bob ThulframJune 24th, 2013 at 18:12daf182June 26th, 2013 at 14:50Vee SatayamasJuly 3rd, 2013 at 02:08Jason WeathersbyJuly 3rd, 2013 at 15:33Vee SatayamasJuly 3rd, 2013 at 20:41Benjamin SchmidtJuly 3rd, 2013 at 04:24Jason WeathersbyJuly 3rd, 2013 at 15:35PlutoJuly 12th, 2013 at 12:30Ron GavioliJuly 16th, 2013 at 05:40Robert Nyman [Editor]July 16th, 2013 at 06:09