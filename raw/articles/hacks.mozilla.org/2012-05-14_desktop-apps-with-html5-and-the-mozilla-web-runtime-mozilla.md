---
title: Desktop Apps with HTML5 and the Mozilla Web Runtime – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2012/05/desktop-apps-with-html5-and-the-mozilla-web-runtime/
author: Joe Stagner
published: '2012-05-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

# Desktop Apps with HTML5

One of the best things about HTML is that it’s never “done”. HTML has been with us longer than most of the development technologies that we consider commonplace. (.NET, ASP, Java, PHP, etc.)

The latest incarnation of HTML, HTML5 has been the source of a great deal of buzz in the software and information industries. When we say “HTML5”, we’re implicitly referring to the “stack” of HTML/CSS/JavaScript.

At Mozilla we often refer to this collectively as the “Web Run-Time” or WebRT for short. [Mozilla’s apps initiative, including the Web Runtime is documented here](https://developer.mozilla.org/en/Apps).

Skeptics like to say “HTML5 is not ready”. This week I saw an article declaring HTML5 won’t be “ready” for another 10 years. To which I ask “ready for what?” Of course there are many APIs that are still under development, but for many scenarios HTML5 is ready now. For many other scenarios its ready for development now and will be ready for general public use in the near future.

Recently the Mozilla Apps Native Install Experience was introduced to the [Firefox Nightly Channel](http://nightly.mozilla.org/). ([Read here for more information about the Firefox release channels.](http://hacks.mozilla.org/2012/05/firefox-and-the-release-channels/))

This functionality lets us install an HTML5 application with a native launching experience on Windows or Mac (Linux and Android coming).

One great way to do this is to simply list your app in the [Mozilla Marketplace](http://hacks.mozilla.org/2012/05/firefox-and-the-release-channels/). The Marketplace will be open to the general public soon and developers can submit their app now at the[ Marketplace Ecosystem Portal](https://marketplace.mozilla.org/en-US/ecosystem/). All you need besides an app to submit is a set of [BrowserID ](https://browserid.org/)credentials.

An HTML5 App that targets the Mozilla Web Runtime includes a manifest file.

The manifest is simply a JSON file that declares certain data about the application.

Here is the manifest file from a sample app. [You can read more about the Mozilla App Manifest here.](https://developer.mozilla.org/en/Apps/Manifest)

```
{
"version": "1.0",
"name": "KO Round Timer",
"description": "A Workout Timer for Fighting Athletes!",
"icons": {
"128": "/images/icon-128.png"
},
"developer": {
"name": "Joe Stagner",
"url": "http://koscience.com"
},
"installs_allowed_from": [
"http://timer.koscience.com",
"https://marketplace.mozilla.org"
],
"default_locale": "en"
}
```

JSON does not need to be formatted with CRLFs. The above JSON is only formatted to simplify display.

Note line #12 above which specifies where the app can be installed from.

The Mozilla Web Runtime includes an apps object ([winbow.navigator.mozApps](https://developer.mozilla.org/en/DOM/window.navigator.mozApps)) The mozApps object (currently implemented in Firefox Nightly on Windows and Mac) has a method to install an application. We’ll look at code that uses that API in a minute.

If you want your app to install from the Mozilla Marketplace you don’t need to write any install code. When you list your app in the marketplace, the marketplace creates a listing page for your app and that page includes an install button.

The generated code that is invoked when the Install button is clicked tells the Runtime to install the app. The Runtime then fetches the manifest for the app and, among other things, checks to see it the app allows installation from whatever domain is requesting the install.

As you can see in the manifest listing above, line 14 specifies that the app may be installed from “https://marketplace.mozilla.org”.

But you might want to let users install your application from other domains, for example your own web site.

You can see line 13 in our sample manifest, listed above, that “http://timer.koscience.com” is also specified as a valid “install from” location. I can specify as many domains as I like to be authorized to install the application from and wildcards are supported.

If we want to install the app from our own web site however, we need to implement the install logic ourselves.

We could create a page similar to the app listing page on the Mozilla Marketplace, or could make the app “self installing” meaning that we could implement installation logic in the app itself.

Take, for example, the Workout Timer app shown below.

Notice the row of navigation buttons at the bottom of the timer.

The last one to the right says “Install Me”.

The install button should only appear if the app is running in an environment that supports the mozApps runtime. Since this app (K.O. Timer) is an HTML5 app it can run in any HTML5 compliant browser but will only be “installable” if it is running in a browser / runtime with mozApps support.

We also don’t want the install button to appear if the app is already installed.

Here is a JavaScript method to test both runtime support and install state.

If runtime support is present and the app is not install then an install button is displayed.

In some scenarios you might choose to forgo the display of an optional install button and simply start the installer when the app is not already installed.

(This code is using jQuery)

```
function TestAppInstalled() {
if ((!navigator.mozApps) || (!navigator.mozApps.getSelf)) {
/*-----------------------------------------------------------+
|| Test to see if the Mozilla Apps Web Runtime is supported
|| HACK: Testing for either mozApps OR mozApps.getSelf is a
|| hack.
|| This is needed because some pre-beta versions of Firefox
|| have the object present but nit fully implemented.
|| TODO: Update when Firefox Desktop & Mobile are complete.
------------------------------------------------------------*/
return;
}
var MyAppSelf = navigator.mozApps.getSelf();
MyAppSelf.onsuccess = function() {
if (! this.result) {
// Application is not "installed"
$('#InstallButton').show();
}
else {
// This "MozApp" is already installed.
}
return;
}
MyAppSelf.onerror = function() {
alert('Error checking installation status: ' +
this.error.message);
return;
}
}
```

When the user clicks on the install button the following code is called.

```
$('#InstallButton').click(function() {
var installation = navigator.mozApps.install(
"http://timer.koscience.com/kotimer.webapp");
installation.onsuccess = function() {
$('#InstallButton').hide();
alert("K.O. Timer has been successfully installed.....");
}
installation.onerror = function() {
alert("APP: The installation FAILED : " + this.error.name);
}
});
```

So when the user navigates to the K.O. Timer app (timer.koscience.com) in a browser that supports mozApps (currently Firefox Nightly) and the user clicks on the “Install Me” button the mozApps runtime starts the installer.

After the user clicks “install” button in the dialog pictured above, the installer is called and, when completed, the user has a native launching experience.

On Windows you get a desktop shortcut.

As well as a Start Menu item.

And, of course the app is now in the user’s Mozilla MyApps collection.

It’s important to remember that, while these launchers have been created on the user’s system the application itself still exists in the cloud. A developer can choose to add “off line” functionality to their application by other HTML5 features like [AppCache](https://developer.mozilla.org/en/Using_Application_Cache), [LocalStorage ](https://developer.mozilla.org/en/DOM/Storage)or [IndexedDB](https://developer.mozilla.org/en/IndexedDB).

The ability to provide native launchers for HTML5 apps, coupled with the huge HTML5 apps distribution mechanism that will be available when the Mozilla Marketplace become available to the general public (in the near future), creates great opportunity for developers building standards based apps.

## 23 comments

Adam MessingerMay 14th, 2012 at 13:56Jean-Yves PerrierMay 14th, 2012 at 15:22Kevin DangoorMay 14th, 2012 at 19:15Adam MessingerMay 16th, 2012 at 09:42Jon GallowayMay 14th, 2012 at 15:11Adam MessingerMay 14th, 2012 at 20:14antistressMay 15th, 2012 at 03:33Joe StagnerMay 15th, 2012 at 07:26antistressMay 15th, 2012 at 08:25pdMay 15th, 2012 at 08:02pdMay 15th, 2012 at 08:26Kevin DangoorMay 16th, 2012 at 06:07alexleducJune 5th, 2012 at 06:08IraêMay 15th, 2012 at 10:18IraêMay 15th, 2012 at 10:22julioMay 16th, 2012 at 17:21Joe StagnerJune 4th, 2012 at 06:38Ken WalkerJuly 9th, 2012 at 11:46LYJuly 26th, 2012 at 23:17Joe StagnerJuly 27th, 2012 at 06:32Tankred HaseJuly 28th, 2012 at 23:22Hayk SaakianJanuary 19th, 2013 at 22:19Robert NymanJanuary 22nd, 2013 at 01:57