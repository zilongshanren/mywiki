---
title: 'App discovery – Firefox OS for developers: the platform HTML5 deserves – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2013/07/app-discovery-firefox-os-for-developers-the-platform-html5-deserves/
author: Chris Heilmann
published: '2013-07-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In the [previous edition of this video series](https://hacks.mozilla.org/2013/06/firefox-os-for-developers-the-platform-html5-deserves/) we introduced FirefoxOS and what it means for the open web and HTML5. We explained that apps for FirefoxOS are HTML5 apps, and could be as simple as a mobile-optimised web site with a [manifest](https://developer.mozilla.org/en-US/docs/Web/Apps/Manifest) file. ![be-the-future](../../assets/b0198161368b9b8c.png)


Now we’re back explaining how Firefox OS is different from other platforms when it comes to app discovery. Here are Mozilla’s principal developer evangelist Chris Heilmann [@codepo8](http://twitter.com/codepo8) and Desigan Chinniah [@cyberdees](http://twitter.com/cyberdees) of the Firefox OS business development team showcasing how easy it is to get your app found on Firefox OS. You can watch the [video on YouTube](http://www.youtube.com/watch?v=QCH_ncCrZfE).

The main difference of app discovery in Firefox OS is that you are not limited to a listing in a closed app store. Being a pure web platform, you can publish your apps either by adding them to the marketplace, but also by adding a simple “install from web” button to your already existing web sites. The code is as simple as adding an event handler to a button that points to your application’s manifest file:

```
var button = document.querySelector('#install');
button.addEventListener('click', function(ev) {
var installapp = navigator.mozApps.install(manifestURL);
installapp.onsuccess = function(data) {
// App is installed
};
installapp.onerror = function() {
// App wasn't installed, info is in
// installapp.error.name
};
}, false);
```

That way you can re-use the work you put into search engine optimisation over the last years and make what you do on the web already advertise for your app.

For end users, the main difference in Firefox OS is that apps can be found in context and locale. The flow for an end user in a closed app environment is the following:

- Go to the marketplace (log in if you aren’t already)
- Pick a promoted app or drill down into a category or search apps by name
- Pick the app, go through the install process, give it the permissions it wants and start the app
- Use it or uninstall it

In any case app discovery is very targeted to the name of the app or dependent on the promotion of the app in the store. Firefox OS works around these problems and instead allows users to find relevant apps with a more intelligent search functionality that also understands locales.

In the case of Firefox OS users can search for a topic, like the name of a band or a movie and find applications that are relevant to that search. For example if you look for a band name, you get Soundcloud for music, Wikipedia for information, Ticketmaster to get tickets for their next concert and many other, relevant apps. This is in the US, in other countries you’d get apps that are relevant there.

Activating any of the icons in the search results then opens this app with the search term you entered, instead of just opening the app and asking you to re-enter your search term. The apps that are loaded are the mobile optimised HTML5 site of that provider, which means they load fast and don’t need to install – it is a real “try before you buy”.

If the user likes the app, they can long-tap and install it, which means you get all the extra functionality Firefox OS offers HTML5 solutions.

In essence, with Firefox OS, we made app discovery as easy as browsing the web, and we give you a very good reason to brush up the mobile optimised web sites you already have on the web.

We hope you enjoy this and that it answers a few of the questions you had about Firefox OS. Watch this space for more videos in this series.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 2 comments

leeoniyaJuly 18th, 2013 at 11:08Janet SwisherJuly 18th, 2013 at 13:24