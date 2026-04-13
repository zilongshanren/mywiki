---
title: Introducing Web Activities – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/01/introducing-web-activities/
author: Robert Nyman
published: '2013-01-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

One of the more powerful things lately for apps on various mobile phones have been intents. Register your app for handling certain types of actions, or specify in your app what kind of support you are looking for, for the thing you are trying to do.

This is especially important in the case of Firefox OS. No matter how good your web app is to begin with, what really takes it to the next level is interaction with other apps and activities on the device.

This is where [Web Activities](https://wiki.mozilla.org/WebAPI/WebActivities) come into place.

It is basically one of the new [WebAPIs](https://wiki.mozilla.org/WebAPI/) we’ve been working on to make the web even more powerful as a platform, and the idea is to have a simple API to both specify intent with your activity, but also declare that your app will be able to handle actions from other apps.

If you haven’t looked into web apps yet, by the way, the best thing is probably to read [Getting started with making apps](https://developer.mozilla.org/en-US/docs/Apps/Getting_Started). In their simplest form, a web app is just HTML5, CSS and JavaScript, with an [app manifest](https://developer.mozilla.org/en-US/docs/Apps/Manifest) added.

## Getting started with Web Activities

There are a few ways you can work with Web Activities:

- Call an activity and get presented with apps that can handle that
- Register your activity support for your web app in the manifest file
- Register activity support on-the-fly
- Attach a handler to your app for when that activity occurs

## Calling an activity

Let’s say you have a button in your app, and you want to be able to get a picture – either from the Gallery, Camera or any other app in Firefox OS that supports that activity. You can then call the `pick`

activity, like this:

```
var pick = new MozActivity({
name: "pick",
data: {
type: ["image/png", "image/jpg", "image/jpeg"]
}
});
```

In this example, we specify the name `pick`

and the data to be PNG or JPEG images. You will then be presented with a menu of available activities in Firefox OS:

![](../../assets/ffad30e0ed4cb0cc.png)


As a user, you choose the app you want to pick an image from – or take a picture with the Camera – and once you’ve done so, the result will be posted back to the requesting app (*Note: it is chosen from within the app handling the activity what, and if, something will be returned*).

## Handling the response

For most WebAPIs, including Web Activities, you will have `onsuccess`

and `onerror`

event handlers. In the case of an image/file you will get a [blob](https://developer.mozilla.org/en-US/docs/DOM/Blob) back. You can then represent that returned image visually directly in your app:

```
pick.onsuccess = function () {
// Create image and set the returned blob as the src
var img = document.createElement("img");
img.src = window.URL.createObjectURL(this.result.blob);
// Present that image in your app
var imagePresenter = document.querySelector("#image-presenter");
imagePresenter.appendChild(img);
};
pick.onerror = function () {
// If an error occurred or the user canceled the activity
alert("Can't view the image!");
};
```

## Register your app for an activity

As mentioned above, you can also set your app as a handler for certain activities. There are two ways to do that:

### Through the manifest file – declaration registration

```
{
"name": "My App",
"description": "Doing stuff",
"activities": {
"view": {
"filters": {
"type": "url",
"url": {
"required": true,
"regexp":"/^https?:/"
}
}
}
}
}
```

### Register an activity handler – dynamic registration

```
var register = navigator.mozRegisterActivityHandler({
name: "view",
disposition: "inline",
filters: {
type: "image/png"
}
});
register.onerror = function () {
console.log("Failed to register activity");
}
```

and then handle the activity:

```
navigator.mozSetMessageHandler("activity", function (a) {
var img = getImageObject();
img.src = a.source.url;
/*
Call a.postResult() or a.postError() if
the activity should return a value
*/
});
```

## Available activities

The available activities to choose from at this time are:

- configure
- costcontrol/balance
- costcontrol/data_usage
- costcontrol/telephony
- dial
- new (e.g. type: “websms/sms”, “webcontacts/contact”)
- open
- pick (e.g. type: “image/png”)
- record
- save-bookmark
- share
- test
- view

A few examples:

### Dial

```
var call = new MozActivity({
name: "dial",
data: {
number: "+46777888999"
}
});
```

### New SMS

```
var sms = new MozActivity({
name: "new",
data: {
type: "websms/sms",
number: "+46777888999"
}
});
```

### New Contact

```
var newContact = new MozActivity({
name: "new",
data: {
type: "webcontacts/contact",
params: { // Will possibly move to be direct properties under "data"
giveName: "Robert",
familyName: "Nyman",
tel: "+44789",
email: "robert@mozilla.com",
address: "Sweden",
note: "This is a note",
company: "Mozilla"
}
}
});
```

### View URL

```
var openURL = new MozActivity({
name: "view",
data: {
type: "url", // Possibly text/html in future versions
url: "http://robertnyman.com"
}
});
```

### Save bookmark

```
var savingBookmark = new MozActivity({
name: "save-bookmark",
data: {
type: "url",
url: "http://robertnyman.com",
name: "Robert's talk",
icon: "http://robertnyman.com/favicon.png"
}
});
```

## Try it out now!

You can try this out right now, by [putting together a web app](https://developer.mozilla.org/en-US/docs/Apps/For_Web_developers) and calling web activities. You can then test it in the [Firefox OS Simulator](https://hacks.mozilla.org/2012/12/firefox-os-simulator-1-0-is-here/)!

## Work in progress

Web Activities are a work in progress, and the activity names, data types etc are subject to change. However, currently most of the above works right now (with the exception for `mozRegisterActivityHandler`

and `mozSetMessageHandler`

, that haven’t been implemented yet).

I hope you share my excitement with all the possibilities Web Activities are offering us, and can probably think of a number of use cases, making your app much more powerful through interaction with other apps!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 33 comments

SteveJanuary 24th, 2013 at 06:31Robert Nyman [Editor]January 24th, 2013 at 12:59SteveJanuary 24th, 2013 at 15:24Jonas SickingJanuary 24th, 2013 at 21:18SteveJanuary 24th, 2013 at 22:42Robert Nyman [Editor]January 25th, 2013 at 02:06Joshua OlsJanuary 24th, 2013 at 07:36Robert Nyman [Editor]January 24th, 2013 at 12:55FabriceJanuary 24th, 2013 at 10:30Robert Nyman [Editor]January 24th, 2013 at 12:55Mikko OhtamaaJanuary 24th, 2013 at 14:00Robert Nyman [Editor]January 24th, 2013 at 14:08RonJanuary 24th, 2013 at 14:45Robert Nyman [Editor]January 24th, 2013 at 15:00Jonas SickingJanuary 24th, 2013 at 21:11PicJanuary 24th, 2013 at 14:45Robert Nyman [Editor]January 24th, 2013 at 15:04SteveJanuary 24th, 2013 at 15:04Robert Nyman [Editor]January 24th, 2013 at 15:08SteveJanuary 24th, 2013 at 15:29Robert Nyman [Editor]January 25th, 2013 at 02:08Joshua OlsJanuary 25th, 2013 at 04:24Robert Nyman [Editor]January 25th, 2013 at 04:38Axel HechtJanuary 25th, 2013 at 05:45Robert Nyman [Editor]January 25th, 2013 at 05:50Jeff WaldenJanuary 27th, 2013 at 03:36Jeff WaldenJanuary 27th, 2013 at 03:39Robert Nyman [Editor]January 28th, 2013 at 08:45Jonas SickingJanuary 29th, 2013 at 02:45Sebastian OrtizJanuary 29th, 2013 at 18:36Robert Nyman [Editor]January 30th, 2013 at 02:12Robin BerjonFebruary 5th, 2013 at 04:30Robert Nyman [Editor]February 5th, 2013 at 07:17