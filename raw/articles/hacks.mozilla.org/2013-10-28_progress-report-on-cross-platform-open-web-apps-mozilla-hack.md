---
title: Progress report on cross-platform Open Web Apps – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/10/progress-report-on-cross-platform-open-web-apps/
author: Ali Almossawi
published: '2013-10-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Here in the Hacks blog we’ve written a lot about [building apps for Firefox OS using HTML, JS, and CSS](https://hacks.mozilla.org/category/apps/). We’re working to ensure that those same apps can also run on Android, Windows, Mac OS X, and Linux devices. If your app can adapt to those screen sizes, CPU’s, and device capabilities, then we’ve got a plan to ensure that your apps install, launch, quit, and uninstall as native apps on each of those platforms.

I’ve created a short video that shows how [Open Web Apps](https://developer.mozilla.org/en/Apps) from Firefox OS will work on any platform where Gecko is available.

Firefox OS is our benchmark platform for Open Web Apps. On Firefox OS, users can discover apps in the Firefox Marketplace and install them directly onto the phone’s home screen. As an example I’m using my app Shotclock, an open web app for computing sun angles for outdoor photographers. Let’s find out what happens when we install this app on other platforms.

## Android

Android users discover apps in Firefox Marketplace using the Firefox for Android browser. Firefox Marketplace has approved Shotclock for Android, so we just click the install button as we did on Firefox OS. We will automatically repackage the Open Web App as a native Android app to give our users a native app experience for Open Web Apps.

Because we installed it from an android APK, we can manage it from the recent app list and we find it in the app drawer like every other app.

## Windows

Windows users discover apps in the Firefox Marketplace using desktop Firefox. Firefox Marketplace has approved Shotclock for Windows laptops too, so we just click the Marketplace install button. We will automatically repackage the open web app as a native Windows app.

Here’s Shotclock running on Windows, just like a real app. Our repackaging will mean that users can launch their open web apps from the Windows Start menu and quit them from the File menu. Users will also uninstall them from the Programs control panel.

## Mac OS X

Mac OS X users also discover apps in the Firefox Marketplace using desktop Firefox. We will automatically repackage the open web app as a native Mac OS X app. When the user clicks the install button, we install Shotclock in the Mac OS X Applications folder.

From there, it launches and runs just like a real app. The native packaging means users can switch between open web apps by pressing Control-Tab, and quit them from the File menu. How much code did the app developer rewrite? Zero.

## Privileged Apps

So far we’ve looked at unprivileged Apps. We will also support privileged apps on all these platforms. Here is Kitchen Sink, our app for testing the Firefox OS privileged APIs. What happens when we install it on Android?

The experience of discovering and installing privileged apps will follow the Android convention of presenting a list of permissions to the user at install time. These permissions are copied from the open web app manifest. After the user completes the installation process, the App is ready to use, and is able to access the phone hardware.

## Linux Desktop

The email application that comes with Firefox OS is basically a privileged App that uses the Socket API for networking. Marco Castelluccio, our open web apps intern, got it running on it on his Linux laptop.

He copied over the app package from Gaia and made one tweak to the app manifest. So, if you like the apps that come with your firefox os phone and want to run them on your other devices, cross-platform open web apps can make that happen.

## iOS

We’d love to support Open Web Apps on iOS devices, but iOS does not, at this time, include the option to install a Gecko-based web browser, which is currently needed to support Open Web Apps.

Edit: We’re working with the Cordova community, both to allow Cordova apps to run unmodified on Firefox OS and to allow Open Web Apps packaged by Cordova to run on iOS. For more details see the [Cordova Firefox OS project page](https://wiki.mozilla.org/CordovaFirefoxOS) and the [Cordova Firefox OS GitHub repository](https://github.com/apache/cordova-firefoxos).

## Timetable

Desktop — You can install hosted, unprivileged apps on your desktops and laptops using Firefox 16 or newer. Privileged app support should land in Firefox Nightly in the next two months.

Android — You can install apps using Mobile Firefox Aurora, but you won’t get a native app experience yet. The native app experience should land in Mobile Firefox Nightly in December.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 29 comments

b3tamaxOctober 28th, 2013 at 10:05Niclas HoyerOctober 28th, 2013 at 10:53Bill WalkerOctober 29th, 2013 at 07:51maddddddddddddddOctober 28th, 2013 at 15:23LukeOctober 28th, 2013 at 21:46BenOctober 29th, 2013 at 03:50AllanOctober 29th, 2013 at 08:00LukeOctober 30th, 2013 at 08:02Bill WalkerOctober 29th, 2013 at 07:42Chris SellsOctober 28th, 2013 at 18:37Bill WalkerOctober 29th, 2013 at 07:47LukeOctober 28th, 2013 at 21:38Bill WalkerOctober 30th, 2013 at 14:49Ivan DejanovicOctober 29th, 2013 at 02:12pdOctober 29th, 2013 at 09:56SteveOctober 29th, 2013 at 14:59Bill WalkerOctober 30th, 2013 at 14:56reProgrammedOctober 29th, 2013 at 15:57pdOctober 30th, 2013 at 01:19Florian Bender (@fbender_dev)October 31st, 2013 at 00:23pdOctober 31st, 2013 at 03:50Robert Nyman [Editor]October 31st, 2013 at 15:58LukeOctober 31st, 2013 at 17:53reProgrammedNovember 10th, 2013 at 16:19JrOctober 30th, 2013 at 05:32Robert Nyman [Editor]October 30th, 2013 at 13:58LukeOctober 31st, 2013 at 17:59nadrimajstorOctober 30th, 2013 at 16:15JuniorNovember 6th, 2013 at 16:14