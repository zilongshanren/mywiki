---
title: What's new in Cordova 3.5.0 for Firefox OS – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/06/whats-new-in-cordova-3-5-0-for-firefox-os/
author: Rodrigo Silveira
published: '2014-06-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The Cordova community recently [released version 3.5.0](http://cordova.apache.org/announcements/2014/05/23/cordova-350.html) of the tools. This version includes some exciting improvements to the Firefox OS development workflow. Before we dive into the new features, make sure you have the latest version by running:

```
$ sudo npm install -g cordova
$ sudo npm install -g plugman
```

Now that we’re all set up, let’s dive into the new features.

## Improved manifest management

In previous versions of Cordova, developers had to manually edit the `manifest.webapp`

file to add permissions and other app information. This file has [crucial information that Firefox OS needs to interact with your app](https://developer.mozilla.org/en-US/Apps/Build/Manifest).

Cordova has a configuration file called `config.xml`

that already contains the same information needed for the manifest file. Cordova will create and update the manifest based on your `config.xml`

file. In the new version, plugins can add configuration specifying which permissions are necessary. Whenever you run a `cordova prepare`

, the manifest is updated based on your configuration. Now you can have all your app’s information in one place.

## Building packages with Cordova

Firefox OS uses web technologies that do not require a compilation step to generate binaries. The related Cordova commands `build`

and `compile`

were left unimplemented and would throw an exception when called. That behavior was confusing and left some people wondering what went wrong.

Now `cordova build`

or `Cordova compile`

will create a zip of your packaged app in the `build`

folder inside the `platform/firefoxos`

folder. A big thank you to the contributor [Gert-Jan Braas](https://github.com/Steckelfisch) for implementing this!

## Plugins

A fresh batch of core plugins [were released too](http://cordova.apache.org/news/2014/06/12/plugins-release.html). We added Firefox OS support to a few more plugins:

To update to the latest version of the plugins, you need to remove and add them again. For example, to use the latest version of the file plugin run:

```
$ cordova plugin rm org.apache.cordova.file
$ cordova plugin add org.apache.cordova.file
```

Replace the plugin name for the plugin you want to update. The [geolocation](https://github.com/apache/cordova-plugin-geolocation/blob/master/doc/index.md) and [contacts](https://github.com/apache/cordova-plugin-contacts/blob/master/doc/index.md) plugins have been updated to support auto managing permissions, make sure you update them too.

Check our [status page](http://mozilla-cordova.github.io/) for updated information on plugin status.

## What’s next

A highly requested feature is support for `emulate`

and `run`

Cordova commands. We are working with the Dev Tools team to create an awesome experience for debugging Cordova applications using Firefox’s App Manager. Here is a sneak preview of what’s coming!

Meanwhile you can debug your app by adding the `platforms/firefoxos/www`

folder to the app manager in Firefox. For more information, check out [Cordova for Firefox OS on MDN](https://developer.mozilla.org/en-US/Apps/Tools_and_frameworks/Cordova_support_for_Firefox_OS).

We are working on creating default icons for a newly created app. They will serve as placeholders that can be easily replaced with your app’s brand.

We also have a [development status page](http://mozilla-cordova.github.io/status/index.html) where you can see up to the minute information on what is being worked on.

We’d love to hear your feedback and feature requests. You can reach us in the [#cordova channel on IRC](ircs://irc.mozilla.org:6697/cordova), or through email at [mozilla-cordova@mozilla.org](mailto:mozilla-cordova@mozilla.org) or log your issues and requests on [the Apache Cordova issue site](https://issues.apache.org/jira/browse/CB/). Also if you are interested in helping out with the project let us know.

## About
[
Rodrigo Silveira ](http://blog.rodms.com)

Works on Mozilla's cross-platform apps team improving Firefox OS support for Cordova and PhoneGap. Passionate about making the web an even better platform for developers. Loves snowboarding, BBQ and beer.