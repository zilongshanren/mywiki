---
title: Better integration for open web apps on Android – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/03/better-integration-for-open-web-apps-on-android/
author: James Hugman
published: '2014-03-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Up until now, developing web apps on mobile has been a little tricky.

After spending the time developing your app, getting your users to install it is difficult, especially when the concept of “installing a web app” is not very well defined.

The most popular method is synonymous with adding a shortcut to the homescreen. This is problematic on a number of fronts, not least because the management of web apps – especially around launching, switching between and uninstalling web apps – differs significantly from that of native apps.

![](../../assets/1d3a60b80df4c21c.png)


*The web app “exists” only on the homescreen, not in the app drawer.*

![](../../assets/1ab5730b5ddaef22.png)


*When it’s running, it is not clearly marked in the Recent Apps list.*

Even once you get something like a smooth user-flow of installing your app onto the user’s phone’s homescreen, you often find that your app is running in a degraded or out-of-date web view, missing out on compatibility or speed optimizations of a desktop class browser.

What we as developers would like is a modern, fast web runtime, which is kept up-to-date on our devices.

Wouldn’t it also be nice for our users to launch and manage their web apps in the same way as native apps?

## Introducing APK Factory

We have been working on making web apps be real on the desktop for some time. On the desktop, if you install a web app, Firefox will repackage the app as a desktop app so that it will integrate perfectly with the rest of your system – as outlined in more detail in [Progress report on cross-platform Open Web Apps](https://hacks.mozilla.org/2013/10/progress-report-on-cross-platform-open-web-apps/).

That means being in the Start menu on Windows, or in the Launch Control screen on Mac OS X.

From Firefox 29, that will apply to Android too.

This means that as a web developer, you can rely on a modern, up-to-date web runtime on Android to run your web apps. Even better, that web runtime is provided by an ordinary Android app, which means it will stay modern and up-to-date, and you can finally say goodbye to the Android Browser.

![](../../assets/7a60a68a642eee4d.png)


*A web app, called ShotClock. Notice its icon in the top right of the screen.*

The user will experience your web app as if it is a real native Android app:

- The app appears in the App Drawer, the Recent Apps list, with its own names and icons,
- The app can be installed and uninstalled just like a native Android app,
- The app can be updated just like a native Android app.

![](../../assets/297d102016eb90f2.png)


*In the App Drawer*

![](../../assets/2042ac7f0e67340d.png)


*In the Recent Apps list: all these apps are web apps*

![](../../assets/f3085863285d701a.png)


*Installed with certain permissions*

Best yet, is that we make these changes without the developer needing to do anything. As a developer, you get to write awesome web apps, and not worry about different packaging needed to deliver the web app to your users.

So if you’re already making first-class apps for Firefox OS, you’re already making first-class apps for Android.

## The Technical details

On Firefox, you can install an app using the `window.navigator.mozApps.install(manifestUrl)`

method call. Any website can use this API, so any website can become an app store.

The `manifestUrl`

is the URL of a `manifest.json`

document which describes the app to your phone without actually loading the app:

- The app’s name and description, translated into any number of languages.
- The app’s icon, in various sizes for different pixel densities.
- The permissions that the app needs to run.
- The WebActivities that the app wants to register.
- For packaged apps only, this provides a URL to the zip file containing the app’s code and resources.

On Firefox for Android, we implement this method by sending the URL to a Mozilla-managed service which builds an Android APK specifically for the app.

APKs created by the Factory use Android’s excellent Resource framework so that the correct icon and translation is displayed to the user, respecting the user’s locale or phone screen.

Web app permissions are rendered as Android permissions, so the user will have a completely native experience of installing your app.

For packaged apps, the APK also includes a copy of the packaged zip file, so that no extra networking is required once the app is downloaded.

For hosted apps, the first time the app is launched, the resources listed in its appcache are downloaded, so that subsequent launches can happen as quickly as possible, without requiring a network connection.

And if you want to detect if the app is running in a web app versus in a webpage, checking the `getSelf()`

method call will help you:

```
if (window.navigator.mozApps) {
// We're on a platform that supports the apps API.
window.navigator.mozApps.getSelf().onsuccess = function() {
if (this.result) {
// We're running in an installed web app.
} else {
// We're running in an webpage.
// Perhaps we should offer an install button.
}
};
}
```

## Keeping your apps up-to-date

For hosted apps, you update your apps as usual: just change your app on your server, and your users will pick up those changes the next time they run your app. You can change as much as you want, and your users will get the latest version of the app each time they launch and connect to your servers.

For anything needing changes to the app’s manifest, your users will get an updated APK sent to them to update their existing installation.

For example, if you want to change the app’s icon, or even name, changing the app’s manifest will cause the APK Factory service to regenerate the app’s APK, and notify your users that there is a new version available for install.

For packaged apps, the same mechanism applies: change the app’s package zip file, then update the version number in the app’s manifest file, and the APK Factory will pick up those changes and notify your users that an updated app is available. Your users will get an notified that there’s a new APK to install. Simples.

## Is that it?

This is an exciting project. It has very little web developer involvement, and no extra API for developers to use: however, it should represent a step forward in usability of web apps on Android.

Now that we have taken the step to generate APKs for web apps, this gives us a platform for further blurring the lines between web apps and apps. Check it out for yourself and help us improve the feature: get [Firefox Beta from the Google Play Store](https://play.google.com/store/apps/details?id=org.mozilla.firefox_beta), install apps from the [Firefox Marketplace](https://marketplace.firefox.com/), and let us know what you think!

## About James Hugman

James is a software engineer who has been working with mobile operating systems since 2009, and with small underpowered computers all his life. At Mozilla he works in the Web Runtime team, spending most of his time persuading the two naughty children "Gecko" and "Android" to play nicely together.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 51 comments

Scott ArciszewskiMarch 20th, 2014 at 11:05Kumar McMillanMarch 21st, 2014 at 01:35Kumar McMillanMarch 21st, 2014 at 01:41Myk MelezMarch 21st, 2014 at 10:11Caspy7March 21st, 2014 at 04:37Myk MelezMarch 21st, 2014 at 10:44Fabricio C ZuardiMarch 21st, 2014 at 14:07Kumar McMillanMarch 21st, 2014 at 14:15Fabricio C ZuardiMarch 21st, 2014 at 14:29Kumar McMillanMarch 21st, 2014 at 14:32Myk MelezMarch 24th, 2014 at 13:24Anthony CameronMarch 25th, 2014 at 19:07Kumar McMillanMarch 26th, 2014 at 16:17Myk MelezMarch 26th, 2014 at 16:20NathanMarch 22nd, 2014 at 07:42Myk MelezMarch 24th, 2014 at 13:37Controlling UserMarch 22nd, 2014 at 13:54Myk MelezMarch 24th, 2014 at 13:39Raymond CamdenMarch 23rd, 2014 at 06:37Kumar McMillanMarch 23rd, 2014 at 07:58Raymond CamdenMarch 23rd, 2014 at 08:12Myk MelezMarch 24th, 2014 at 13:51Raymond CamdenMarch 24th, 2014 at 14:15Raymond CamdenMarch 24th, 2014 at 14:16Raymond CamdenMarch 24th, 2014 at 14:19Myk MelezMarch 24th, 2014 at 16:33Caspy7March 24th, 2014 at 17:26JamesMarch 23rd, 2014 at 06:57James HugmanMarch 23rd, 2014 at 07:32Kumar McMillanMarch 23rd, 2014 at 08:00JamesMarch 23rd, 2014 at 08:21Kumar McMillanMarch 23rd, 2014 at 08:23JamesMarch 23rd, 2014 at 09:24Anthony CameronMarch 23rd, 2014 at 12:56Wes JohnstonMarch 25th, 2014 at 08:54Anthony CameronMarch 25th, 2014 at 09:54Myk MelezMarch 25th, 2014 at 17:30d00dMarch 24th, 2014 at 08:03Myk MelezMarch 24th, 2014 at 14:09Mathis GardonMarch 25th, 2014 at 10:23Myk MelezMarch 25th, 2014 at 17:25Brian LePoreMarch 24th, 2014 at 10:27Anthony CameronMarch 24th, 2014 at 10:38Myk MelezMarch 24th, 2014 at 14:56Anthony CameronMarch 25th, 2014 at 10:06Wes JohnstonMarch 25th, 2014 at 12:33EnriqueApril 9th, 2014 at 04:48Kumar McMillanApril 9th, 2014 at 08:06Myk MelezApril 14th, 2014 at 15:32EnriqueApril 15th, 2014 at 00:24Myk MelezApril 18th, 2014 at 08:15