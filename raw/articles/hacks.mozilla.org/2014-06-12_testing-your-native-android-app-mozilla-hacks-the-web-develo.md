---
title: Testing Your Native Android App – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/06/testing-your-native-android-app/
author: Austin King
published: '2014-06-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It’s an interesting time to be a web developer!

For years Apps have been eating the web and now we are seeing the Web eat the OS. Mozilla is pushing for a world where you can write standards-based, [Open Web Apps](https://developer.mozilla.org/en/Apps). These apps should install as native apps and just work, regardless of the platform.

With the new [Firefox for Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox), we will now automatically convert your Open Web App into a native Android app.

But how can you test you app on Android, before you submit it to the [Marketplace](http://marketplace.firefox.com/)?

We have a new tool to add to your lineup!

## Introducing mozilla-apk-cli

If you have [NodeJS](http://nodejs.org/) as well as [zip/unzip](http://info-zip.org/) installed, then you can use our new command line tool to build testable .apk installers.

`mozilla-apk-cli`

is a command-line application, so the commands below would be run from a terminal application.

Getting setup is easy:

`npm install mozilla-apk-cli`

This will give you a new program `mozilla-apk-cli`

available in `./node_modules/.bin/`


You can also globally install with

`npm install -g mozilla-apk-cli`

I’ll assume you put `./node_modules/.bin`

in your path or installed globally.

Open Web Apps come in three flavors and the CLI can build them all:

- hosted app
- packaged app zip file
- packaged app from a directory of source code

Let’s assume you have a [packaged app](https://developer.mozilla.org/en-US/Marketplace/Publishing/Packaged_apps) you are working on.

You have a directory layout like this:

```
www/
index.html
manifest.webapp
css/
style.css
i/
icon-256.png
icon-128.png
icon-60.png
js/
main.js
```

You can build a testable Android app with the following:

`mozilla-apk-cli ./www my_test_app.apk`

This will produce `my_test_app.apk`

which can be side-loaded to your phone in either of the following ways:

- Put in on the web and download/install form a browser on your Android device
- Use adb to install the app

`adb install my_test_app.apk`

Setting up `adb`

is out of scope for this blog post, but [the Android SDK site](http://developer.android.com/sdk/index.html) has some good [resources on adb](http://developer.android.com/tools/help/adb.html).

## Distribution

**Do not distribute this test .apk file**!!!

If you change your app, rebuild and send the APK to your users, the update will fail to install. With each new version of your app, using Android’s app manager, you have to remove the test app before installing the 2nd version.

`mozilla-apk-cli`

is *only* for testing and debugging your new Android app locally. When you are happy with your app, you should distribute the Open Web App through the [Marketplace](http://marketplace.firefox.com/) or [from your website](https://developer.mozilla.org/en-US/Marketplace/Options/Self_publishing) via an install page.

You don’t need to manage an .apk file directly. Just like you don’t need to manage Mac OS X, Windows or Linux builds for your Open Web App.

We’ve baked native Android support deeply into the Firefox for Android runtime. When a user chooses to install an Open Web App, the native app is **synthesized on demand** using the production APK Factory Service. This works regardless of the website or Marketplace you are installing the Open Web App from.

## How does the CLI work?

Back to our new test tool. This tool is a frontend client to the [APK Factory Service](https://wiki.mozilla.org/Mobile/Projects/APK_Factory). It takes your code and sends it to a **reviewer** instance of the service. Reviewer as opposed to the **production release** environment.

This service synthesizes an native Android app, builds it with the Android SDK and lastly signs it with a development cert. As mentioned, this synthesized APK is **debuggable** and **should not be distributed**.

The nice thing about the service is that you do not have to have Java, ant, the Android SDK and other Android development tools installed on your local computer. You can focus on the web and test on whatever devices you have handy.

## Hosted and Packaged Zip files

We just looked at how to test a packaged app which is a directory of source code. Now lets look at the other two modes. If you already have built your packaged app into a .zip file, use:

`mozilla-apk-cli ./my_app.zip my_test_app.apk`

If you are building a hosted app, use:

`mozilla-apk-cli http://localhost:8080/ my_test_app.apk`

## No Android Devices? No stress

Perhaps you are saying "Sounds cool, but I don’t have any Android devices… How am I supposed to test?"

Good point. We’re enabling this automatically.

**On the one hand**, don’t worry. One thing [mobile first development](http://www.abookapart.com/products/mobile-first) has taught us, is that there are **way more devices** and platforms that you will ever have testing resources for. The web is about open standards and progressive enhancement.

Your web app is just going to be a little bit nicer as a native android app, fitting into the OS as the user expects.

It doesn’t use native UI widgets or anything like that, so extensive testing is not required. The rendering engine is gecko from the already installed Firefox for Android.

**On the other hand**… open standards and compatibility is a nice story, but as web developers, we know things tend to have platform specific bugs. I’d recommend the traditional grading of supported platforms and if Android is a high priority, definitely get a device, Firefox for Android and test your app.

As we make native experiences automatic across platforms (Android, Mac OS X, etc) we are all ears for feedback. What do you think?

## mozilla-apk-cli Resources

The [source code for the CLI tool is on GitHub](https://github.com/mozilla/apk-cli). If you need a sample packaged app, [here is a demo version](http://github.com/ozten/packaged-app/). The [source code for the APK Factory Service is also on GitHub](https://github.com/mozilla/apk-factory-service).

Join us in [with ideas, feedback and questions](ircs://irc.mozilla.org:6697/apkfactory) and please file bugs in [Marketplace Integration](https://bugzilla.mozilla.org/enter_bug.cgi?product=Marketplace&component=Integration).

*Thanks to Wil Clouser for the illustrations.*

## About
[
Austin King ](http://ozten.com)

Seattle based non-dogmatic Artist / Programmer type human. Rogue web developer with the Apps Engineering team. Spell check is for the week.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 17 comments

SekanderJune 12th, 2014 at 02:41Austin KingJune 12th, 2014 at 09:40Antoine TurmelJune 12th, 2014 at 02:48Fawad HassanJune 12th, 2014 at 03:18Austin KingJune 12th, 2014 at 09:32David BruantJune 12th, 2014 at 02:58Austin KingJune 12th, 2014 at 09:02ThomasJune 12th, 2014 at 05:49RobertJune 12th, 2014 at 06:36LukeJune 12th, 2014 at 07:22RobertJune 12th, 2014 at 09:04Bill WalkerJune 12th, 2014 at 10:05Mte90June 12th, 2014 at 06:50Austin KingJune 12th, 2014 at 08:57Austin KingJune 12th, 2014 at 08:53ThomasJune 12th, 2014 at 09:08Myk MelezJune 12th, 2014 at 09:55