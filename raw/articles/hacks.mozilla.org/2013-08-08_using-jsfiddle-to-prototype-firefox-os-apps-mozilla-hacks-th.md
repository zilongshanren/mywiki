---
title: Using JSFiddle to Prototype Firefox OS Apps – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/08/using-jsfiddle-to-prototype-firefox-os-apps/
author: Angelina Fabbro
published: '2013-08-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Dancing to the Tune of the Fiddle

JSFiddle is a fantastic prototyping and code review tool. It’s great for getting out a quick test case or code concept without having to spool up your full tool chain and editor. Further, it’s a great place to paste ill-behaved code so that others can review it and ideally help you get at the root of your problem.

Now you’re able to not only prototype snippets of code, but Firefox OS apps as well. We’re very excited about this because for a while now we’ve been trying to make sure developers understand that creating a Firefox OS app is just like creating a web app. By tinkering with JSFiddle live in your browser, we think you’ll see just how easy it is and the parallels will be more evident.

## Fiddling a Firefox OS App: The Summary

Here are the steps that you need to go through to tinker with Firefox OS apps using JSFiddle:

- Write your code as you might normally when making a JSFiddle
- Append /webapp.manifest to the URL of your Fiddle URL to and then paste this link into the Firefox OS simulator to install the app
- Alternatively, append /fxos.html to your Fiddle URL to get an install page like a typical Firefox OS hosted application

I’ve created a demo JSFiddle [here](http://jsfiddle.net/afabbro/vrVAP/) that we will go over in detail in the next section.

## Fiddling a Firefox OS App: In Detail

### Write Some Code

Let’s start with a basic “Hello World!”, a familiar minimal implementation. Implement the following code in your Fiddle:

**HTML:**

```
```# Hello world!


**CSS**

```
h1 {
color: #f00;
}
```

**JavaScript**

```
alert(document.getElementsByTagName('h1')[0].innerHTML);
```

Your Fiddle should resemble the following:

Then, append /manifest.webapp to the end of your Fiddle URL. Using my demo Fiddle as an example, we end up with http://jsfiddle.net/afabbro/vrVAP/manifest.webapp

Copy this URL to your clipboard. Depending on your browser behavior, it may or may not copy with ‘http://’ intact. Please note that the simulator will not accept any URLs where the protocol is not specified explicitly. So, if it’s not there – add it. The simulator will highlight this input box with a red border when the URL is invalid.

If you try and access your manifest.webapp from your browser navigation bar, you should end up downloading a copy of the auto-generated manifest that you can peruse. For example, here is the manifest for my test app:

```
{
"version": "0",
"name": "Hello World Example",
"description": "jsFiddle example",
"launch_path": "/afabbro/vrVAP/app.html",
"icons": {
"16": "/favicon.png",
"128": "/img/jsf-circle.png"
},
"developer": {
"name": "afabbro"
},
"installs_allowed_from": ["*"],
"appcache_path": "http://fiddle.jshell.net/afabbro/vrVAP/cache.manifest",
"default_locale": "en"
}
```

If you haven’t written a manifest for a Firefox OS app before, viewing this auto-generated one will give you an idea of what bits of information you need to provide for your app when you create your own from scratch later.

### Install the App in the Simulator

Paste the URL that you copied into the field as shown below. As mentioned previously, the field will highlight red if there are any problems with your URL.

After adding, the simulator should boot your app immediately.

You can see that after we dismiss the alert() that we are at a view (a basic HTML page in this case) with a single red **h1** tag as we would expect.

### Install the App From a Firefox OS Device

In the browser on your Firefox OS device or in the browser provided in the simulator, visit the URL of your Fiddle and append /fxos.html. Using the demo URL as an example again, we obtain: [http://jsfiddle.net/afabbro/vrVAP/fxos.html](http://jsfiddle.net/afabbro/vrVAP/fxos.html)

Click install, and you should find the app on your home screen.

## Caveats

This is still very much a new use of the JSFiddle tool, and as such there are still bugs and features we’re hoping to work out for the long term. For instance, at time of writing this article, the following caveats are true:

- You can only have one JSFiddle’d app installed in the simulator at a time
- There is no offline support

## Thanks

This JSFiddle hack comes to us courtesy of Piotr Zalewa, who also happens to be working on making PhoneGap build for Firefox OS. Let us know what you think in the comments, and post a link to your Fiddle’s manifest if you make something interesting that you want to show off.

## About
[
Angelina Fabbro ](http://realityhacking.net)

I'm a developer from Vancouver, BC Canada working at Mozilla as a Technical Evangelist and developer advocate for Firefox OS. I love JavaScript, web components, Node.js, mobile app development, and this cool place I hang out a lot called the world wide web. Oh, and let's not forget Firefox OS. In my spare time I take singing lessons, play Magic: The Gathering, teach people to program, and collaborate with scientists for better programmer-scientist engagement.

## 8 comments

AlexandraAugust 9th, 2013 at 00:01VedaAugust 9th, 2013 at 04:25zalunAugust 9th, 2013 at 15:28VedaAugust 27th, 2013 at 23:06Dom FinnAugust 9th, 2013 at 06:00firefos.ruAugust 9th, 2013 at 12:31CarlosAugust 17th, 2013 at 18:21Olivier BridgemanAugust 27th, 2013 at 10:59