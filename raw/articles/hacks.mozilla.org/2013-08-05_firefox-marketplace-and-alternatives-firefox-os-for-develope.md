---
title: 'Firefox Marketplace and alternatives – Firefox OS for developers: the platform
  HTML5 deserves – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2013/08/firefox-marketplace-and-alternatives-firefox-os-for-developers-the-platform-html5-deserves/
author: Chris Heilmann
published: '2013-08-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In the fourth video of our “Firefox OS – the platform HTML5 deserves” series ([part one](https://hacks.mozilla.org/2013/06/firefox-os-for-developers-the-platform-html5-deserves/), [part two](https://hacks.mozilla.org/2013/07/app-discovery-firefox-os-for-developers-the-platform-html5-deserves/) and [part three](https://hacks.mozilla.org/?p=21869) have already been published) we talk about how to submit apps to the Firefox Marketplace, and explain alternative ways to distribute your apps.

![Firefox OS - be the future](../../assets/b0198161368b9b8c.png)


Here are Mozilla’s principal developer evangelist Chris Heilmann ([@codepo8](http://twitter.com/codepo8)) and Desigan Chinniah ([@cyberdees](http://twitter.com/cyberdees)) of the Firefox OS business development team showcasing how easy it is to get your app published on Firefox OS. You can watch the [video on YouTube](https://www.youtube.com/watch?v=RlD-yRhUMPY).

Firefox OS – like any other mobile platform – has a [marketplace](https://marketplace.firefox.com/) that allows you to find apps by name or category.

As a developer, to submit your app to the marketplace all you have to do to is to create a [manifest file](https://developer.mozilla.org/en-US/docs/Web/Apps/Manifest) and host it on your server (make sure to give it the correct MIME type “application/x-web-app-manifest+json”). In the manifest you define name of your app, provide icons and ask for permission to access [web activities](https://wiki.mozilla.org/WebAPI/WebActivities) and other functionality. You can [validate your manifest online](https://marketplace.firefox.com/developers/validator) before going further to avoid erroneous submissions.

Once you have your manifest in place, you can [submit your app](https://developer.mozilla.org/en-US/docs/Web/Apps/Publishing/Submitting_an_app) to the marketplace. There you provide screenshots or videos and a longer description of your app.

If the app is hosted on your server, you get all the HTML5 functionality you expect to get. You don’t get access to the camera or the contact book though. To get this, you need to package your app and host it on the marketplace. You can get more information on the [different levels of app privileges on the Wiki](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/Security/Security_model#Trusted_and_Untrusted_Apps).

As your apps are HTML5 apps you can also install them directly from the web without having to go through the marketplace. This also means that we don’t break the link-ability of the Web – you can send someone a link that will trigger the app install on a device that allows for the [Open WebApps standards proposal](https://developer.mozilla.org/en-US/docs/Web/Apps/JavaScript_API) (Firefox OS or Android with Firefox installed). This proposal is part of the [WebAPI proposals](https://wiki.mozilla.org/WebAPI) and allows you to create a “install this app” button with a few lines of code:

```
if (navigator.mozApps) {
function install() {
var installapp = navigator.mozApps.install(manifestURL);
installapp.onsuccess = function(data) {
// App is installed
};
installapp.onerror = function() {
// Something went wrong,
// information is in: installapp.error.name
};
}
var button = document.createElement('button');
button.innerHTML = 'Install this app';
button.addEventListener('click', install, false);
document.body.appendChild('button');
}
```

This allows you to re-use all the effort you put into promoting your existing web presence to become the advertisement for your app.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!