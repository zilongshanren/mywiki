---
title: Localizing the Firefox OS Boilerplate App – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/01/localizing-the-firefox-os-boilerplate-app/
author: Ckoehler; Robert Nyman Posted; Localization
published: '2014-01-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As Firefox OS devices are launched in more and more countries and apps become available to users of all different languages, it becomes increasingly important to consider localizing your app. Making your app available in more languages is one of the best ways to make your app available and relevant to more users.

As such, we’re piloting a program to help developers not only localize their apps, but also connect them with localizers. If you’re an interested developer or localizer, please [get in touch](mailto:appsdev@mozilla.com?subject=App Localization) and we’ll tell you more about how to join our program.

Localizing is generally a straight-forward process, and consists of two main steps:

- preparing your app for localization (sometimes called internationalization)
- obtaining translations of relevant app content

There are many approaches to localization. Many of you are probably already familiar with gettext-based libraries. Jed is one such implementation specifically designed for html and JavaScript-based applications. Mozilla is also leading a next-generation localization project called L20n. In this article, we build upon the method we [previously mentioned](https://hacks.mozilla.org/2013/08/localizing-firefox-os-apps/) using the webl10n.js library also employed by Gaia, the UI layer for Firefox OS and show you how we localized the [Firefox OS Boilerplate App](https://github.com/robnyman/Firefox-OS-Boilerplate-App).

![Firefox OS Boilerplate App, localized in French Firefox OS Boilerplate App, localized in French](../../assets/aeb5ade9d9349541.png)

### Setup

If you’d like to follow along, clone the [Firefox OS Boilerplate App](https://github.com/robnyman/Firefox-OS-Boilerplate-App), which is available on Github:

`clone https://github.com/robnyman/Firefox-OS-Boilerplate-App.git`

As mentioned, we used the version of Fabien Cazenave’s [webL10n.js](https://github.com/fabi1cazenave/webL10n/) library that is available in the Gaia source tree ([direct link](https://github.com/mozilla-b2g/gaia/blob/master/shared/js/l10n.js)). In your own projects, feel free to use either version. Not sure which to use? [Read this.](https://github.com/fabi1cazenave/webL10n/wiki/webL10n-vs-Gaia-webL10n)

First, I navigated to the directory that contains all application JavaScript and then download l10n.js:

```
[Firefox OS App Boilerplate/js]$
wget https://github.com/mozilla-b2g/gaia/blob/master/shared/js/l10n.js
```

Then I created a directory to contain all locale information:

```
[Firefox OS App Boilerplate/]$
mkdir locales
```

This is where we store files that contain both the base, and the translated strings for the Boilerplate App.

Now, in that directory, I created the locales initialization file. You can name this anything you like. I selected locales.ini, which is what many of the Gaia apps use:

```
[Firefox OS App Boilerplate/locales]$
touch locales.ini
```

In that file, I began by specifying which property file to import for the default language, which in our case is en-US:

```
@import url(en-us/app.properties)
```

The import line for your default locale should always be the first line of this file.

It’s up to you how to name and organize your properties files. For the Firefox OS Boilerplate, I chose to have each property file be named app.properties and be stored in its own directory, name for its locale. Here’s what the beginning of the locales/ directory looks like:

```
├── ar
│ ├── app.properties
│ └── manifest.properties
├── de
│ ├── app.properties
│ └── manifest.properties
├── el
│ └── manifest.properties
├── en-US
│ ├── app.properties
│ └── manifest.properties
```

This structure makes working with our chosen translation platform, Transifex, easier. We’ll explain Transifex along with those manifest.properties files a bit later on.

As new locales are added, the locales.ini file needs to be updated. Here are lines I added for the ar and de locales:

```
[ar]
@import url(ar/app.properties)
[de]
@import url(de/app.properties)
```

Each import statement needs to be preceded by a heading with the relevant locale code in square brackets. This tells l10n.js which import statements to use for which locales.

Next, I edited the main app file, index.html, to include the l10n.js library and to specify which initialization file to use. In the head section, I added:

```
```

At this point I checked to make sure everything was still loading as expected, which it was. The easiest way to check your work as you go is to use the [Firefox OS Simulator](https://developer.mozilla.org/en-US/docs/Tools/Firefox_OS_Simulator).

### Indicating translatable content with data-l10n-id tags

One advantage of using l10n.js is that any elements specified as needing translation are translated automatically upon page load without the user having to select a locale. The library determines the locale based on the system locale (e.g., which locale the user selected when they completed the first run experience).

The way that you specify which elements should be translated is by giving them data-l10n-id attributes. For example, I indicated that the h1 heading "Firefox OS Boilerplate App" needed translation with the following:

```
```##
Firefox OS Boilerplate App


The value that you give this data-l10n-id attribute will become a key in your properties file. In en-us/app.properties, I added a corresponding line for this heading:

`app-heading = Firefox OS Boilerplate App`

For your default locale, the value assigned to this key will be identical to what it is in your app. But for other locales, it will be translated. Here’s what the corresponding line looks like for de/app.properties:

`app-heading = Firefox OS Boilerplate App in Deutsch!`

Any element with text that you want to localize can and should be given an data-l10n-id attribute and then a corresponding line should be added to your default locale properties file. This can be tedious to do after you have created a lot of application code, so you might consider writing a script to help you out. (I have one in the works, but it’s not fit for consumption yet).

### Retrieving translated strings with JavaScript

Sometimes you will need to access localized strings within JavaScript. When you do this, in order to be sure the L10n.js library is available, you’ll need to wrap your functions with the the navigator.mozL10n.ready() function. The following code snippet enables the localization of a notification that is created via JavaScript:

```
navigator.mozL10n.ready ( function () {
// grab l10n object
var _ = navigator.mozL10n.get;
// Notifications
var addNotification = document.querySelector("#add-notification");
if (addNotification) {
addNotification.onclick = function () {
var appRef = navigator.mozApps.getSelf(),
icon;
appRef.onsuccess = function (evt) {
icon = appRef.result.manifest.icons["16"];
console.log("I am: " + icon);
var notification = navigator.mozNotification.createNotification(
_('notification-text'),
icon,
icon
);
notification.show();
var img = document.createElement("img");
img.src = icon;
document.body.appendChild(img);
};
};
}
});
```

If you don’t follow this method, you can’t be sure that your JavaScript will be parsed after the l10n library is completely initialized.

### Localizing the manifest

After tagging all elements with data-l10n-id attributes and adding corresponding lines to my en-us/app.properties file, it was then time to make some changes to the manifest.webapp.

The first change was to make sure a [default locale](https://developer.mozilla.org/en-US/Apps/Developing/Manifest#default_locale) was specified:

`"default_locale": "en",`

This property refers to the locale of the manifest itself. It is used primarily by the Marketplace to determine how to parse the manifest. It is not used by the device the app is installed on or the Firefox OS simulator. MDN recommends that whatever locale is used here is **not** included in the ‘locales’ property. Instead, the name and description for the default locale is specified in ‘name’ and ‘description’ fields which are always required.

Next, I added a ‘locales’ property:

```
"locales": {
}
```

As new locales are added, it’s necessary to update the `locales`

property with a localized version of the app name and description. These values are used not only by the Firefox OS user interface, but also the Firefox Marketplace. To accomplish this, I created separate manifest.properties files in each of my locales directories. Having separate files for each locales makes it easier for localizers to work on the project and also makes it easier for me to manage. When a localizer completes a new locale, I copy the values to the manifest.webapp file. This is something that could be easily scripted, however.

This is the translated de/manifest.properties file:

```
name=Firefox OS Boilerplate App in Deutsch!
description=Boilerplate Firefox OS App mit Beispiel Anwendungsfälle, um loszulegen
```

And the updated ‘locales’ property in manifeset.webapp:

```
"locales": {
"de": {
"name": "Firefox OS Boilerplate App",
"description": "Boilerplate Firefox OS App mit Beispiel Anwendungsfälle, um loszulegen"
}
}
```

## Managing Localization Process with Transifex

With the Boilerplate, we started a pilot program to explore the use of [Transifex](https://www.transifex.com/) for managing translations. If you visit our [team page](https://www.transifex.com/organization/mozilla-tech-evangelism/) there, you’ll see the Boilerplate along with a handful of other apps from developers who have joined us there.

### Why Transifex?

In looking at l10n platforms, we wanted one that would support both paid and volunteer translations as well as one that would support a wide range of localization formats and workflows. Transifex fit that profile. We’re also very excited about [Pontoon](https://github.com/mathjazz/pontoon) a platform currently in development by our l10n team and look forward to using with the Boilerplate and other apps when it’s ready.

### Creating the project

Once signed up and logged in to Transifex, creating a project is easy. You specify a project name, description, source language and license. If you indicate that your license is open source, you’ll be prompted for the link to your app’s source code.

![Creating a project on Transifex](../../assets/574d7962205df89b.png)


![Creating a project on Transifex](../../assets/574d7962205df89b.png)

### Configuring Transifex (tx config)

I like to work from the command line, so I used the Transifex client ([installation details](http://support.transifex.com/customer/portal/articles/995605-installation)) for the following steps, but you can do the following steps from the Transifex website as well.

Working in the root of my Firefox OS Boilerplate App directory, I first initiated the Transifex project:

```
[Firefox OS App Boilerplate/]$
tx init
```

This command creates a `.tx`

directory and a `config`

file within it.

When first setting up a project to work with Transifex, you’ll need to set some values in this config file.

The `.tx/config`

file for the Boilerplate looks like this:

```
[main]
host = https://www.transifex.com
[firefox-os-boilerplate.app_properties]
file_filter = locales/
```/app.properties
source_file = locales/en-US/app.properties
source_lang = en
type = MOZILLAPROPERTIES
minimum_perc = 50
[firefox-os-boilerplate.manifest_properties]
file_filter = locales//manifest.properties
source_file = locales/en-US/manifest.properties
source_lang = en
type = MOZILLAPROPERTIES
minimum_perc = 50

Each block of the config is indicted with square brackets. A project on Transifex can have any number of resources, so you can organize your app in the way that you like.

For the Boilerplate, we have two resources:

**firefox-os-boilerplate.app_properties**, which maps to the file app.properties and includes all of the strings from the app that we want to localize.**firefox-os-boilerplate.manifest_properties**, which maps to the file manifest.properties and includes the localize name and description that we’ll copy to the manifest.webapp

Resources are also listed in the Transifex web interface:

![Firefox OS Boilerplate language resources](../../assets/a2b8b643bf42c8af.png)


![Firefox OS Boilerplate language resources](../../assets/a2b8b643bf42c8af.png)

In Transifex, each resource will be copied when a new language is requested. Translators then check out those files, edit them to include their translations and then check them back in when they are done.

Other options are:

**file_filter**: Tells Transifex how you have organized your locale files. For the boilerplate, I wanted each property file to have the same name and be sorted into directories named after each locale. Transifex substitues locale forto acheive this. **source_file**: Tells transifex what is the source of strings (default locale).**source_lang**: Indicates the locale of the source file (e.g the default project locale).**type**: Indicates what file type you are using for translation. Transifex supports a[number of options](http://support.transifex.com/customer/portal/articles/971979-supported-file-formats).**minimum_perc**: Sets the threshold value for when Transifex will pull in a new locale. 50 means that a locale must be at least 50% complete before Transifex will pull the locale into your project.

Once the config file was completed, I pushed it to Transifex with:

```
[Firefox OS App Boilerplate/]$
tx push -s
Pushing translations for resource firefox-os-boilerplate.app_properties:
Pushing source file (locales/en-US/app.properties)
Resource does not exist. Creating...
Pushing translations for resource firefox-os-boilerplate.manifest_properties:
Pushing source file (locales/en-US/manifest.properties)
Resource does not exist. Creating...
Done.
```

### Workflow

Once the Boilerplate project was setup to use Transifex, I was able to use the client to pull and push new / updated translations:

```
[Firefox OS App Boilerplate/]$
tx pull
Pulling translations for resource firefox-os-boilerplate.app_properties (source: locales/en-US/app.properties)
-> ar: locales/ar/app.properties
-> id: locales/id/app.properties
Pulling translations for resource firefox-os-boilerplate.manifest_properties (source: locales/en-US/manifest.properties)
Done.
```

Transifex works seemlessly with any revision control system. We use git for the Firefox OS Boilerplate, and our workflow looks like:

- Use
`tx pull`

to bring in new translations from Transifex (could also download them via the web interface). - Commit and push changes vwith git.
- Repeat.

We can also accept localizations via git and them push them to Transifex.

Note: When using Transifex, I recommend that you keep your .tx config directory in your project’s code repo. You’ll want anyone checking out your project to use this information to properly sync with Transifex. No secret information is contained in .tx/config (rather, that’s in ~/.transifexrc).

### Invitation to participate!

If you are a developer interested in localizing your app, or a localizer interested in contributing translations, we’d love to [hear from you](mailto:appsdev@mozilla.com?subject=App Localization)! We also invite you to join our team on Transifex if you’d like to connect with other developers and translators who are working on localization of Firefox OS apps.

## About
[
ckoehler ](http://christiekoehler.com)

Open culture evangelist, writer, programmer, community builder, vegan, queer, anti-oppressionist, Buddhist, Mozillian, and co-founder of Stumptown Syndicate. Based in Portland, OR, USA.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 5 comments

goofyJanuary 21st, 2014 at 14:17Robert Nyman [Editor]January 22nd, 2014 at 05:43Matjaž HorvatJanuary 22nd, 2014 at 03:30Robert Nyman [Editor]January 22nd, 2014 at 05:43Tom ChapmanJanuary 28th, 2014 at 20:18