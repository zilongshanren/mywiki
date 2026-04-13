---
title: Taking pictures with the Camera API – part of WebAPI – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2012/04/taking-pictures-with-the-camera-api-part-of-webapi/
author: Robert Nyman
published: '2012-04-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Through the [Camera API](https://developer.mozilla.org/en/DOM/Using_the_Camera_API), part of [WebAPI](https://wiki.mozilla.org/WebAPI), it becomes possible to take pictures with your device’s camera and upload them into the current web page. This is achieved through an `input`

element with `type="file"`

and an `accept`

attribute to declare that it accepts images.

The HTML looks like this:

```
```

![](../../assets/3fb0c140f4f12655.png)


After the picture has been taken, the user is presented with a choice to accept or discard it. If accepted, it gets sent to the `<input type="file">`

element and its `onchange`

event is triggered.

## Get a reference to the taken picture

With the help of the [File API](https://developer.mozilla.org/en/Using_files_from_web_applications) you can then access the taken picture/chosen file:

```
var takePicture = document.querySelector("#take-picture");
takePicture.onchange = function (event) {
// Get a reference to the taken picture or chosen file
var files = event.target.files,
file;
if (files && files.length > 0) {
file = files[0];
}
};
```

## Presenting the taken picture in the web page

Once we have a reference to the taken picture (i.e. file) we can then use [createObjectURL](https://developer.mozilla.org/en/Document_Object_Model_%28DOM%29/window.URL.createObjectURL) to create a URL referencing the picture and setting it to the `src`

of an image:

```
// Image reference
var showPicture = document.querySelector("#show-picture");
// Get window.URL object
var URL = window.URL || window.webkitURL;
// Create ObjectURL
var imgURL = URL.createObjectURL(file);
// Set img src to ObjectURL
showPicture.src = imgURL;
// For performance reasons, revoke used ObjectURLs
URL.revokeObjectURL(imgURL);
```

If `createObjectURL`

isn’t supported, an alternative is to fallback to [FileReader](https://developer.mozilla.org/en/DOM/FileReader):

```
// Fallback if createObjectURL is not supported
var fileReader = new FileReader();
fileReader.onload = function (event) {
showPicture.src = event.target.result;
};
fileReader.readAsDataURL(file);
```

## Complete example demo and code

If you want a complete working example page, I’ve created a [Camera API demo](http://robnyman.github.com/camera-api/). Here is the code for the HTML page and its accompanying JavaScript file:

### HTML page

```
```Camera API
# Camera API

A demo of the Camera API, currently implemented in Firefox and Google Chrome on Android. Choose to take a picture with your device's camera and a preview will be shown through createObjectURL or a FileReader object (choosing local files supported too).


## Preview:




### JavaScript file

```
(function () {
var takePicture = document.querySelector("#take-picture"),
showPicture = document.querySelector("#show-picture");
if (takePicture && showPicture) {
// Set events
takePicture.onchange = function (event) {
// Get a reference to the taken picture or chosen file
var files = event.target.files,
file;
if (files && files.length > 0) {
file = files[0];
try {
// Get window.URL object
var URL = window.URL || window.webkitURL;
// Create ObjectURL
var imgURL = URL.createObjectURL(file);
// Set img src to ObjectURL
showPicture.src = imgURL;
// Revoke ObjectURL
URL.revokeObjectURL(imgURL);
}
catch (e) {
try {
// Fallback if createObjectURL is not supported
var fileReader = new FileReader();
fileReader.onload = function (event) {
showPicture.src = event.target.result;
};
fileReader.readAsDataURL(file);
}
catch (e) {
//
var error = document.querySelector("#error");
if (error) {
error.innerHTML = "Neither createObjectURL or FileReader are supported";
}
}
}
}
};
}
})();
```

## Web browser support

- Camera API is currently supported in Firefox and Google Chrome on Android devices.
- createObjectURL is supported in Firefox, Google Chrome and Internet Explorer 10+.
- FileReader is supported in Firefox, Google Chrome, Internet Explorer 10+ and Opera 11.6+.

## The future

With WebRTC – which is support for real time, audio, video & data communications between two browsers – and a `navigator.getUserMedia`

approach we will see much more of this in the near future, in a number of the major web browsers. For more information, please see our [Web Platform Roadmap for Firefox](https://wiki.mozilla.org/Platform/Roadmap).

But for now, you can enjoy taking/capturing pictures!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 12 comments

John DrinkwaterApril 3rd, 2012 at 02:05Robert NymanApril 3rd, 2012 at 06:48Prasanna VenkadeshAugust 20th, 2012 at 07:08Prasanna VenkadeshAugust 20th, 2012 at 07:18Robert NymanAugust 20th, 2012 at 11:49WoldenJune 5th, 2012 at 04:48Robert NymanJune 5th, 2012 at 05:40WoldenJune 5th, 2012 at 17:58WoldenJune 5th, 2012 at 18:07Robert NymanJune 6th, 2012 at 23:07david knikolsJune 22nd, 2012 at 14:43Robert NymanJune 25th, 2012 at 06:33