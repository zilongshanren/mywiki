---
title: How to install packaged apps in Firefox OS – options and tools – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2013/03/how-to-install-packaged-apps-in-firefox-os-options-and-tools/
author: Robert Nyman
published: '2013-03-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I thought this would be a good time to show the options for developers how to install packaged apps, and as an extension to that, installing them on an actual Firefox OS device (more on [Open Web apps](https://hacks.mozilla.org/2013/02/getting-started-with-open-web-apps-why-and-how/), if it’s new to you).

## Why a packaged app?

First and foremost, a [packaged app](https://developer.mozilla.org/en-US/docs/Apps/Packaged_apps) is where all resources in your app is zipped into one file, that gets installed directly on the device. That means that all the files are available directly, without needing an Internet connection.

The other benefit is that if you need to access some privileged APIs for your app, it needs to be a packaged app to get access to those (for security reasons, since code hosted anywhere on the web naturally can’t have access to sensitive APIs on the device).

The different APIs are outlined in the [Using WebAPIs to make the web layer more capable](https://hacks.mozilla.org/2013/02/using-webapis-to-make-the-web-layer-more-capable/) article and the permissions needed for each API are listed in [App permissions](https://developer.mozilla.org/en-US/docs/Apps/App_permissions).

## Testing in the Firefox OS Simulator

In the [Firefox OS Simulator](https://addons.mozilla.org/en-US/firefox/addon/firefox-os-simulator/) – latest features listed in [previewing version 3.0](https://hacks.mozilla.org/2013/03/firefox-os-simulator-previewing-version-3-0/) – you have the option to install your app as a packaged app.

In the Simulator Dashboard, you have a button with the label Add Directory. When you do that, and point to the `manifest.webapp`

for your app, it automatically gets installed as a packaged app. Simple as that!

Not all APIs are supported in the Firefox OS Simulator, but it’s a good start!

When you push the update button, the app should be refreshed and restarted if already running, and started if not running. If the content or the manifest is not updated after an “update” click, there’s a blocking error, shown in the Simulator Dashboard.

![](../../assets/2cefc3b9bfa8039f.png)


## Push to Device in the Simulator

As we described here before, one of the new features in [version 3.0 of the Firefox OS Simulator](https://hacks.mozilla.org/2013/03/firefox-os-simulator-previewing-version-3-0/) is the feature Push to Device.

If you have Firefox OS device connected when you use the Firefox OS Simulator, you will get a Push button next to each app in the Simulator Dashboard to push it directly to your app.

You will then need to accept that incoming request on the device to install the app.

![image](../../assets/ce96e9fbdab60963.png)


### Manual steps

- Once you’ve pushed the app to the device, you need to manually close and restart it again, to get updated content
- If you update anything in the manifest, e.g. app name, orientation, you need to reboot the operating system for those changes to have effect

### Things to think about

- Remote debugging has to be enabled on the device, via
`Settings > Device information > More Information > Developer > Remote debugging`

- For Windows support, make sure to install the
[necessary drivers](http://developer.android.com/tools/extras/oem-usb.html)and that you use the latest version of the Firefox OS Simulator (currently, that means the[3.0 preview](https://hacks.mozilla.org/2013/03/firefox-os-simulator-previewing-version-3-0/)). - On Linux (at least Ubuntu), you must create the file
`/etc/udev/rules.d/51-android.rules`

as root and then add a manufacturer-specific entry for the device as described by[Android’s Setting up a Device for Development](http://developer.android.com/tools/device.html#setting-up). Example for one of our test devices:entry:

`SUBSYSTEM=="usb", ATTR{idVendor}==" 19d2", MODE="0666", GROUP="plugdev"`

- Make sure you have the latest version of Firefox OS on your device (especially due to recent fixes like
[bug 842725](https://bugzilla.mozilla.org/show_bug.cgi?id=842725))

## Use make-fxos-install and command line

If you want to establish a good workflow and you’re a fan of the terminal, we’d like to recommend using [make-fxos-install](https://github.com/digitarald/make-fxos-install) by [Harald Kirschner](http://digitarald.de/). It’s a command-line tool to easily push apps directly to a device.

### Step 1

- Install
[XULRunner](http://ftp.mozilla.org/pub/mozilla.org/xulrunner/releases/18.0.2/sdk/) - Install
[Android SDK](http://developer.android.com/sdk/index.html)

### Step 2

Clone the [make-fxos-install](https://github.com/digitarald/make-fxos-install) repository.

### Step 3

Go into your local `make-fxos-install`

directory on the command line.

### Choose what app type to install

Your two options are packaged or hosted. You need to call a make command and point to the folder of your app. For example:

```
make FOLDER=../Firefox-OS-Boilerplate-App packaged install
```

Alternatively:

```
make FOLDER=../Firefox-OS-Boilerplate-App hosted install
```

Accept the prompt on the device, and that’s it!

![image](../../assets/1c4cf21d0a200b04.png)


Please note that the packaged app will have all files in your app, while the hosted app alternative only needs two files to be installed:

- A
`manifest.webapp`

file - A
`metadata.json`

file

Then in the `metadata.json`

file you only need to set the `manifestURL`

parameter from where the app should be served.

### Manual steps

The same steps as described above for Push to Device in the Firefox OS Simulator applies:

Close and restart app to see changes, and an updated manifest = rebooting the OS to see any of those changes.

## Test it out!

Please test out the above solutions and see what works best for you (we realize it might be a little while before you get access to an actual device). let us know what works and what doesn’t – we’d love to hear your feedback!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.

## One comment

VladApril 9th, 2013 at 00:35