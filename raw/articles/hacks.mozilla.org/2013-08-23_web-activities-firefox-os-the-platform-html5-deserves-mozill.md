---
title: 'Web Activities – Firefox OS: the platform HTML5 deserves – Mozilla Hacks -
  the Web developer blog'
url: https://hacks.mozilla.org/2013/08/web-activities-firefox-os-the-platform-html5-deserves/
author: Chris Heilmann
published: '2013-08-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In the sixth video of our “Firefox OS – the platform HTML5 deserves” series (the previous [five videos are published here](https://hacks.mozilla.org/category/videoseries/)) we talk about how [Web Activities](https://wiki.mozilla.org/WebAPI/WebActivities) allow you as a developer to access parts of the hardware without having to package your app.

![Firefox OS - be the future](../../assets/b0198161368b9b8c.png)


Check out the video featuring Chris Heilmann ([@codepo8](http://twitter.com/codepo8)) from Mozilla and Daniel Appelquist ([@torgo](http://twitter.com/torgo)) from [Telefónica Digital](http://blog.digital.telefonica.com)/ W3C talking about the why and how of Web Activities. You can [watch the video here](http://youtu.be/SLL9WSQj4Yg).

[Web Activities](https://wiki.mozilla.org/WebAPI/WebActivities) are a way to extend the functionality of HTML5 apps without having to access the hardware on behalf of the user. In other words, you don’t need to ask the user to access the camera or the phone, but instead your app asks for an image or initiate a call and the user then picks the app most appropriate for the task. In the case of a photo the user might pick it from the gallery, the wallpapers or shoot a new photo with the camera app. You then get the photo back as a file blob. The code is incredibly simple:

```
var pick = new MozActivity({
name: "pick",
data: {
type: ["image/png", "image/jpg", "image/jpeg"]
}
});
```

You invoke the “pick” activity and you ask for an image by listing all the MIME types you require. This small script will cause a Firefox OS device or an Android device running Firefox to show the user the following dialog:

![pick dialog](../../assets/ffad30e0ed4cb0cc.png)


All activities have a success and failure handler. In this case you could create a new image when the user successfully picked a source image or show an alert when the user didn’t allow you to take a picture or it was the wrong format:

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

Other Web Activities work in a similar fashion, for example to ask the user to call a number you write the following:

```
var call = new MozActivity({
name: "dial",
data: {
number: "+46777888999"
}
});
```

This opens the application the user has defined as the one to make phone calls, and asks to call the number. Once the user hangs up, you get a success handler object back.

Web Activities have a few benefits:

**They allow secure access to hardware**– instead of asking the user to allow yet another app to use the camera you send the user to the application they already trust to do this.**They allow your app to be part of the user’s device experience**– instead of building a camera interface you send the user to the one they already are familiar with to take photos**You allow apps to become an ecosystem on the device**– instead of having each app do the same things, you allow them to specialise on doing one thing and one thing well**You keep the user in control**– they can provide you with the photo from anywhere they want and they can store results from your app’s functionality where they want rather than in yet another database on their device

We’ve covered the subject here before in detail in the [Introducing Web Activities](https://hacks.mozilla.org/2013/01/introducing-web-activities/) post.

The simplest way to get started with Web Activities on a Firefox OS device (or simulator) or an Android phone running Firefox is to download the [Firefox OS Boilerplate App](https://github.com/robnyman/Firefox-OS-Boilerplate-App) and play with the activities and the code:

![Firefox OS Boilerplate App](../../assets/fcdc835ab26396b2.jpeg)


Web Activities are a simple way to enable the apps hosted on your servers to reach further into the hardware without acting on behalf of the user. Instead, you let users decide how to get the information you want and concentrate on what to do with the data once you have it instead.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 7 comments

Ivan DejanovicAugust 23rd, 2013 at 01:42Bingo RomnaiaAugust 25th, 2013 at 10:01Robert Nyman [Editor]August 26th, 2013 at 20:40felixAugust 29th, 2013 at 14:07LennieAugust 31st, 2013 at 04:34skierpageSeptember 11th, 2013 at 19:16Robert Nyman [Editor]September 12th, 2013 at 02:42