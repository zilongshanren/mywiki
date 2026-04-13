---
title: PhoneGap Developer App preview for Firefox OS – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/09/phonegap-developer-app-preview-for-firefox-os/
author: Rodrigo Silveira
published: '2014-09-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The cross-platform team at Mozilla is always looking for ways to improve how developers build apps with open web standards. We consider [Cordova](http://cordova.io) and [PhoneGap](http://phonegap.com/) to be great tools to achieve that. We are excited to work on improving support for PhoneGap by getting [the PhoneGap Developer App](http://app.phonegap.com/) into Firefox OS.

The PhoneGap Developer App allows you to easily run PhoneGap apps in multiple platforms, without the need to install SDKs or have a developer subscription. The app is available for Android, iOS and Windows Phone at their respective app stores. You can pair your app with multiple devices at a time and any changes you make to your app’s code get propagated to all devices.

Even though developing for Firefox OS does not require a beefy SDK or a developer subscription, being able to have your changes propagate to multiple devices at once is pretty cool!

We have started working on support for Firefox OS and you can try it out today. In this post we’re going through the steps needed to get the preview version of the PhoneGap developer app in Firefox OS. As they say, a video is worth 1k images:

## Getting the dependencies

We will be using a development version of [Cordova](http://cordova.apache.org/) combined with a development version of the [PhoneGap command line interface](http://phonegap.com/) to get it all working. Luckily, they are very compatible and work well together. You will need to have [git](http://git-scm.com/downloads), [nodejs and npm ](http://nodejs.org/download/)installed before proceeding.

Let’s first get all modules we’ll need from github:

```
$ git clone https://github.com/apache/cordova-firefoxos.git
$ git clone https://github.com/apache/cordova-cli.git
$ git clone https://github.com/apache/cordova-lib.git
$ git clone -b fxos https://github.com/rodms10/phonegap-app-developer.git
$ git clone -b fxos https://github.com/rodms10/connect-phonegap.git
$ git clone https://github.com/phonegap/phonegap-cli.git
```

Now let’s set dependencies up:

```
$ cd connect-phonegap
$ npm link
$ cd ../phonegap-cli
$ npm link connect-phonegap
$ npm install
$ cd ../cordova-lib/cordova-lib
$ npm link
$ cd ../../cordova-cli
$ npm link cordova-lib
$ npm install
$ cd ..
```

## Load the app to your device

The app is available at `phonegap-app-developer/platforms/firefoxos/www/`

, just point the [app manager](https://developer.mozilla.org/en-US/Firefox_OS/Using_the_App_Manager) or [webIDE](https://developer.mozilla.org/en-US/docs/Tools/WebIDE) to this path and load it to your device or simulator. Once you start the app, you should see a screen with an IP address. That’s where you enter the address of your server.

## Starting the server

Let’s get the server going. It will serve your app’s content to the PhoneGap Developer App. Create a new Cordova app:

```
$ cordova-cli/bin/cordova create myapp org.app.my "I Heart PhoneGap Dev App"
$ cd myapp
```

Now we need to point cordova to the development version of `cordova-firefoxos`

. In your root app folder, `myapp`

in our case, create a folder named `.cordova`

(with the leading dot) and add a file named `config.json`

to the new folder with the following contents:

```
{
"lib": {
"firefoxos": {
"uri": "/<Full/Path/To>/cordova-firefoxos",
"version": "dev",
"id": "cordova-firefoxos-dev"
}
}
}
```

Make sure you have the correct full path to `cordova-firefoxos`

in the `uri`

property above.

Time to start the server, we’ll switch back to PhoneGap for that:

```
$ ../phonegap-cli/bin/phonegap.js serve
```

You should see a line saying `[phonegap] listening on 10.0.0.1:3000`

. Enter that IP in the PhoneGap Developer App and see your app start running there! Easy.

## Ship It!

If you got this far, you’re probably asking why isn’t the app in the marketplace already! As you saw, to get all up an running we required the development version of the PhoneGap command line interface. Once a new version with our new code is released, we can publish the app and not require development version of the command line.

If you have any questions leave a comment, find us at the [#apps channel on IRC](ircs://irc.mozilla.org:6697/apps) or send us an email at [mozilla-cordova@mozilla.org](mailto:mozilla-cordova@mozilla.org).

## About
[
Rodrigo Silveira ](http://blog.rodms.com)

Works on Mozilla's cross-platform apps team improving Firefox OS support for Cordova and PhoneGap. Passionate about making the web an even better platform for developers. Loves snowboarding, BBQ and beer.

## 9 comments

AnandhamoorthySeptember 2nd, 2014 at 10:08Rodrigo SilveiraSeptember 2nd, 2014 at 10:51ErikSeptember 2nd, 2014 at 11:34AdamSeptember 3rd, 2014 at 07:30Rodrigo SilveiraSeptember 3rd, 2014 at 10:23AdamSeptember 2nd, 2014 at 13:17dynamisSeptember 4th, 2014 at 09:54Rodrigo SilveiraSeptember 4th, 2014 at 09:57aaronrajaSeptember 5th, 2014 at 07:35