---
title: Getting started with Open Web Apps – why and how – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2013/02/getting-started-with-open-web-apps-why-and-how/
author: Robert Nyman
published: '2013-02-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We’ve been talking a lot about [Open Web Apps](http://www.mozilla.org/apps/), [Firefox OS](http://www.mozilla.org/firefoxos/) and more here lately, and I wanted to cover both how to get started, and, maybe more importantly, why.

## Why a web app?

If we look at the climate for mobile development, it has usually come down to a choice where developers had to pick their platform and skill. Maybe do iOS and Objective-C, or Android and Java.

The big challenge here, of course, is that if you want to deliver your content on several platforms, you’ve had a few choices:

- Pick one platform, and ignore the others
- Learn a number of programming languages
- Have separate development teams for each platform

For major organizations, having multiple teams has been something they could do, while many other have struggled with that. And naturally, many mobile apps are in addition to a company/service web site, just adding more and more on top of the things that need to be maintained, supported and developed.

Therefore, for reasons like saving costs, simplicity of one development language and more, many developers have jumped on the options like [PhoneGap](http://phonegap.com/), [Titanium](http://www.appcelerator.com/platform/titanium-sdk/) and more, thus developing with HTML5 and JavaScript, and then packaging it for various mobile operating systems.

This has been a good and interesting approach, but probably far from optimal in most cases. We at Mozilla want you to be able to use your existing skills as a web developer, but instead of having you jump through hoops to make it work, we want the platforms to evolve and give you more possibilities and power.

This is accomplished by giving you as a developer access to a large amount of [WebAPIs](https://wiki.mozilla.org/WebAPI), [Web Activities](https://hacks.mozilla.org/2013/01/introducing-web-activities/) and more, to make the web layer as powerful a platform as it deserves to be.

The idea with Open Web Apps is not to make you choose a new platform or, worse, excluding others – on the contrary, it’s about giving you means to reuse your existing code and, if desired, make small additions to make it installable as an app.

## Should I build an app?

While many other platforms have a strong interest in getting you tied into their platform, delivering to their app store etc, I would rather say that the first question you need to ask yourself is:

Do I really need to make an app out of this?


In some cases, yes, definitely! But in other cases, you need to be professional and come to the conclusion that it is probably not likely to add any extra value – a few use cases where you don’t need to do an app have been outlined in articles like [No, I’m not going to download your bullshit app](http://tommorris.org/posts/8070) and [Packaged HTML5 Apps: Are we emulating failure?](http://groovecoder.com/2013/01/07/packaged-html5-apps-are-we-emulating-failure/).

I don’t want to trick you into making an app just for the sake of it, or that you’ll do it just because others do. I would rather see you make a fair assessment, and if your app idea has something additional to offer to the end user and overall user experience, then you should consider doing an app.

So, what could those cases be? A few of them might be:

- You want to offer a richer experience than you could offer from a web page, e.g. accessing some WebAPIs specific to the platform/device
- You need to store a lot of information in localStorage or IndexedDB
- The user wants to have a real installation
- The user wants a nice icon on their home screen/desktop for easier accessibility

## Types of Open Web Apps

There are basically two types of Open Web Apps you can install:

- Hosted apps
- Packaged apps

### Hosted apps

Hosted apps are apps running from a URL, but in an app context. This means that you need to be online to run it, and all resources (e.g. files, images etc) will reside on your server and where you will host it.

One option to avoid the need for connectivity is [make sure your app works offline](https://developer.mozilla.org/en-US/docs/HTML/Using_the_application_cache). This is done by adding an appcache file with listings of assets to be made available offline, and then refer to it from your main page:

#### HTML file

#### Appcache file

```
CACHE MANIFEST
# Version 1.0
index.html
css/base.css
js/base.js
js/webapp.js
js/offline.js
NETWORK:
*
FALLBACK:
/ fallback.html
```

For learning more about offline support and caveats, I strongly recommend looking into these resources:

#### Pros

- You completely control the update process
- Just run/reuse currently existing code

#### Cons

- Requires connectivity (if offline support isn’t implemented)
- Doesn’t have as much access to APIs as a packaged app

### Packaged apps

[Packaged apps](https://developer.mozilla.org/en-US/docs/Apps/Packaged_apps) are where you put all your assets in a ZIP file, and then offer that as a complete package to be installed. This makes these files available at all times, and it also gives you elevated privileges – i.e. you can access more APIs – since all the code can be security cleared before install.

#### Pros

- Available offline by default
- More API access

#### Cons

- More difficult to maintain
- Update process for getting new versions out

At the end of the day, you need to evaluate your needs, workflow, APIs you need to work with and more to make a good decision whether you want to do a hosted or a packaged app.

## Getting started with Open Web Apps

After all that talk, what do you actually need to build an Open Web App? Not much, as it turns out. We’ve documented it on MDN in [Getting started with making apps](https://developer.mozilla.org/en-US/docs/Apps/Getting_Started) but I’d like to give you a quick run-down here as well.

Basically, all you need to do is take an existing web site/service you have and add a manifest file. Voilà, that’s it! Yes, really. And to get it installed, of course.

### The manifest file

A manifest file describes your app, with things like name, icons, developer and such, but also localization support, path to launch, permission request for certain APIs and more. All manifest fields are available in [App manifest on MDN](https://developer.mozilla.org/en-US/docs/Apps/Manifest).

A simple manifest could look like this:

```
{
"version": "1",
"name": "Firefox OS Boilerplate App",
"launch_path": "/Firefox-OS-Boilerplate-App/index.html",
"description": "Boilerplate Firefox OS app with example use cases to get started",
"icons": {
"16": "/Firefox-OS-Boilerplate-App/images/logo16.png",
"32": "/Firefox-OS-Boilerplate-App/images/logo32.png",
"48": "/Firefox-OS-Boilerplate-App/images/logo48.png",
"64": "/Firefox-OS-Boilerplate-App/images/logo64.png",
"128": "/Firefox-OS-Boilerplate-App/images/logo128.png"
},
"developer": {
"name": "Robert Nyman",
"url": "http://robertnyman.com"
},
"installs_allowed_from": ["*"],
"default_locale": "en"
}
```

Save this file with a .webapp extension, for instance, `manifest.webapp`

. One very important thing to note here is that this file needs to be served with the `Content-type`

: `application/x-web-app-manifest+json`

.

This is something you need to set up on your server, e.g. through an [.htaccess file](http://en.wikipedia.org/wiki/Htaccess) in Apache:

`AddType application/x-web-app-manifest+json .webapp`

Once you have your manifest, make sure to [validate your app](https://marketplace.firefox.com/developers/validator) to see that it has the correct format.

### Installing the app

Now that your manifest is in order and served with the right `Content-type`

, let’s offer a way to install it. In your web page, you can add an install button that calls this code:

```
var installApp = navigator.mozApps.install(manifestURL);
// Successful install
installApp.onsuccess = function(data) {
console.log("Success, app installed!");
};
// Install failed
installApp.onerror = function() {
console.log("Install failednn:" + installApp.error.name);
};
```

Make sure that the URL to the manifest is absolute – a simple way to do this is to extract the URL from the current page with the install button, and to have the `manifest`

file in the same location:

```
var manifestURL = location.href.substring(0, location.href.lastIndexOf("/")) + "/manifest.webapp";
```

Optionally, you can also provide a second parameter to the `install`

method, receipts, which is a JSON object. More on that in the [documentation for the install method](https://developer.mozilla.org/en-US/docs/DOM/Apps.install).

### Installing a packaged app

The above solution, with a manifest file and an install call, works well with hosted apps. With Packaged apps, you need to go through some extra steps:

#### ZIP all app content

Make sure to ZIP all the files (not the containing folder), including the regular manifest file. The manifest file *has* to be named `manifest.webapp`


#### Create a mini manifest

Create another manifest file, for instance named package.webapp, and make sure the `package_path`

is absolute to where the ZIP file is located.

Also, developer name and info has to match between mini manifest and the regular one in the ZIP file.

```
{
"name": "Firefox OS Boilerplate App",
"package_path" : "http://localhost/Firefox-OS-Boilerplate-App/Firefox-OS-Boilerplate-App.zip",
"version": "1",
"developer": {
"name": "Robert Nyman",
"url": "http://robertnyman.com"
}
}
```

#### Installing a package

Instead of using the regular `install`

method, you now call the `installPackage`

method, which points to the mini manifest, which in turn points to the ZIP file/package:

```
var manifestURL = location.href.substring(0, location.href.lastIndexOf("/")) + "/package.webapp";
var installApp = navigator.mozApps.installPackage(manifestURL);
```

#### Turning on Developer Mode

For this to work in the [Firefox OS Simulator](https://hacks.mozilla.org/2012/12/firefox-os-simulator-1-0-is-here/), you need to turn on the Developer Mode:

```
Settings > Device Information > More Information >
Developer > Developer mode
```


*Note: this is a work in progress, and the availability of this option might vary, and not be available in your version of the Simulator or an actual Firefox OS device.*

#### Specifying permissions

If you plan on using some APIs that only Packaged apps have access to, you need to add a couple of things to your regular (manifest.webapp) file:

- Add type property (e.g. “type” : “privileged”)
- Specify permission access

```
"permissions": {
"contacts": {
"description": "Required for autocompletion in the share screen",
"access": "readcreate"
},
"alarms": {
"description": "Required to schedule notifications"
}
}
```

There is also an interesting option, in the form of [packaged-app-server](https://github.com/robhudson/packaged-app-server), which offers zipping the files as a package when they get requested at run time.

```
$ cd ~/myapp
$ python ~/serve_packaged_apps.py
```

## An example app

As an example app – if you want to check out something easy to dissect, tweak and get started with – feel free to test the [Firefox OS Boilerplate App](https://hacks.mozilla.org/2013/01/introducing-the-firefox-os-boilerplate-app/). It supports:

- An install button, offering you to install it as a hosted app
[Web Activities](https://hacks.mozilla.org/2013/01/introducing-web-activities/)– lots of examples and use cases[WebAPIs](https://wiki.mozilla.org/WebAPI)in action- Offline support (disabled by default)
- Packaged apps – install your app as a ZIP file

## Which platforms are supported?

Let’s look at where we are right now with Open Web Apps. They are supported in:

### Firefox OS

You can install an Open Web App in Firefox OS (the Simulator or on a device) and most WebAPIs and Web Activities will work.

![image](../../assets/30f01a2d0a025456.png)


### Firefox on Android

In [Firefox on Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox&hl=en) you can install an app, and have it installed on your home screen with the correct icon. However, it doesn’t support the WebAPIs and Web Activities.

![image](../../assets/1d50080dcd47f39f.png)


### Nightly/Aurora versions on Desktop

You can install and run a stand-alone app in [Firefox Nightly](http://nightly.mozilla.org/)/[Firefox Aurora](http://www.mozilla.org/en-US/firefox/aurora/), but it doesn’t have access to many WebAPIs and no Web Activities.

![image](../../assets/e998b1af8fa3cd18.png)


The initial strong focus at the moment is support on mobile, but the hope and goal is that Open Web Apps will work on all platforms and devices, by adding support to needed APIs and more.

## Marketplace

When it comes to Open Web Apps, you can use or install them from anywhere. Completely up to you.However, if you are interested in being listed, hosted and much more, I recommend taking a look at the [Firefox Marketplace](https://marketplace.firefox.com/).

You can also visit the [Developer Hub](https://marketplace.firefox.com/developers/) for a lot more information about app development.

## Conclusion

Open Web Apps aren’t here to change your developing ways – they are here to give you the option to install your existing web solutions as apps, access device-specific APIs and more.

Don’t reinvent the wheel – just make it a bit more powerful!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 14 comments

Brian LePoreFebruary 5th, 2013 at 10:11Robert Nyman [Editor]February 5th, 2013 at 13:07SergeiFebruary 6th, 2013 at 07:24Robert Nyman [Editor]February 6th, 2013 at 07:26Stefan KienzleFebruary 8th, 2013 at 04:37Robert Nyman [Editor]February 8th, 2013 at 05:35Stefan KienzleFebruary 8th, 2013 at 06:25Robert Nyman [Editor]February 12th, 2013 at 03:37Stefan KienzleFebruary 14th, 2013 at 01:15Robert Nyman [Editor]February 14th, 2013 at 05:50Christophe RouxFebruary 20th, 2013 at 06:45Robert Nyman [Editor]February 20th, 2013 at 07:10Christophe RouxFebruary 22nd, 2013 at 01:32Robert Nyman [Editor]February 22nd, 2013 at 01:50