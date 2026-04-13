---
title: How to develop a HTML5 Image Uploader – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/01/how-to-develop-a-html5-image-uploader/
author: Paul Rouget
published: '2011-01-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*HTML5 comes with a set of really awesome APIs. If you combine these APIs with the <canvas> element, you could create a super/modern/awesome Image Uploader. This article shows you how.*

*All these tips work well in Firefox 4. I also describe some alternative ways to make sure it works on Webkit-based browsers. Most of these APIs don’t work in IE, but it’s quite easy to use a normal form as a fallback.*

*Please let us know if you use one of these technologies in your project!*

# Retrieve the images

## Drag and drop

To upload files, you’ll need an [<input type=”file”>](https://developer.mozilla.org/en/HTML/element/input#attr-type) element. But you should also allow the user to drag and drop images from the desktop directly to your web page.

I’ve written a detailed article about [implementing drag-and-drop support for your web pages](http://hacks.mozilla.org/2009/12/file-drag-and-drop-in-firefox-3-6/).

Also, take a look at the [Mozilla tutorial on drag-and-drop](https://developer.mozilla.org/en/Using_files_from_web_applications#Selecting_files_using_drag_and_drop).

## Multiple input

Allow the user the select several files to upload at the same time from the File Picker:

```
```

Again, here is an article I’ve written about [multiple file selection](http://hacks.mozilla.org/2009/12/multiple-file-input-in-firefox-3-6/).

# Pre-process the files

## Use the File API

(See the [File API documentation](https://developer.mozilla.org/en/using_files_from_web_applications) for details.)

From drag-and-drop or from the [<input>](https://developer.mozilla.org/en/HTML/element/input) element, you have a list a files ready to be used:

```
// from an input element
var filesToUpload = input.files;
// from drag-and-drop
function onDrop(e) {
filesToUpload = e.dataTransfer.files;
}
```

Make sure these files are actually images:

```
if (!file.type.match(/image.*/)) {
// this file is not an image.
};
```

## Show a thumbnail/preview

There are two options here. You can either use a [FileReader](https://developer.mozilla.org/en/DOM/FileReader) (from the File API) or use the new [ createObjectURL()](https://developer.mozilla.org/en/DOM/window.URL.createObjectURL) method.

### createObjectURL()

```
var img = document.createElement("img");
img.src = window.URL.createObjectURL(file);
```

### FileReader

```
var img = document.createElement("img");
var reader = new FileReader();
reader.onload = function(e) {img.src = e.target.result}
reader.readAsDataURL(file);
```

## Use a canvas

Once you have the image preview in an [<img>](https://developer.mozilla.org/en/HTML/element/img) element, you can draw this image in a [<canvas>](https://developer.mozilla.org/en/HTML/element/canvas) element to pre-process the file.

```
var ctx = canvas.getContext("2d");
ctx.drawImage(img, 0, 0);
```

## Resize the image

People are used to uploading images straight from their camera. This gives high resolution and extremely heavy (several megabyte) files. Depending on the usage, you may want to resize such images. A super easy trick is to simply have a small canvas (800×600 for example) and to draw the image tag into this canvas. Of course, you’ll have to update the canvas dimensions to keep the ratio of the image.

```
var MAX_WIDTH = 800;
var MAX_HEIGHT = 600;
var width = img.width;
var height = img.height;
if (width > height) {
if (width > MAX_WIDTH) {
height *= MAX_WIDTH / width;
width = MAX_WIDTH;
}
} else {
if (height > MAX_HEIGHT) {
width *= MAX_HEIGHT / height;
height = MAX_HEIGHT;
}
}
canvas.width = width;
canvas.height = height;
var ctx = canvas.getContext("2d");
ctx.drawImage(img, 0, 0, width, height);
```

## Edit the image

Now, you have your image in a canvas. Basically, the possibilities are infinite. Let’s say you want to apply a sepia filter:

```
var imgData = ctx.createImageData(width, height);
var data = imgData.data;
var pixels = ctx.getImageData(0, 0, width, height);
for (var i = 0, ii = pixels.data.length; i < ii; i += 4) {
var r = pixels.data[i + 0];
var g =pixels.data[i + 1];
var b = this.pixels.data[i + 2];
data[i + 0] = (r * .393) + (g *.769) + (b * .189);
data[i + 1] = (r * .349) + (g *.686) + (b * .168)
data[i + 2] = (r * .272) + (g *.534) + (b * .131)
data[i + 3] = 255;
}
ctx.putImageData(imgData, 0, 0);
```

# Upload with XMLHttpRequest

Now that you have loaded the images on the client, eventually you want to send them to the server.

## How to send a canvas

Again, you have two options. You can [convert the canvas to a data URL](https://developer.mozilla.org/en/DOM/HTMLCanvasElement) or (in Firefox) [create a file from the canvas](https://developer.mozilla.org/en/Code_snippets/Canvas#Saving_a_canvas_image_to_a_file).

### canvas.toDataURL()

```
var dataurl = canvas.toDataURL("image/png");
```

### Create a file from the canvas

```
var file = canvas.mozGetAsFile("foo.png");
```

## Atomic upload

Allow the user to upload just one file or all the files at the same time.

## Show progress of the upload

Use the upload events to create a progress bar:

```
xhr.upload.addEventListener("progress", function(e) {
if (e.lengthComputable) {
var percentage = Math.round((e.loaded * 100) / e.total);
// do something
}, false);
```

## Use FormData

You probably don't want to just upload the file (which could be easily done via: `xhr.send(file)`

) but add side information (like a key and a name).

In that case, you'll need to create a `multipart/form-data`

request via a [ FormData](https://developer.mozilla.org/en/XMLHttpRequest/FormData) object. (See

[Firefox 4: easier JS form handling with FormData](http://hacks.mozilla.org/2010/05/formdata-interface-coming-to-firefox/).)

```
var fd = new FormData();
fd.append("name", "paul");
fd.append("image", canvas.mozGetAsFile("foo.png"));
fd.append("key", "××××××××××××");
var xhr = new XMLHttpRequest();
xhr.open("POST", "http://your.api.com/upload.json");
xhr.send(fd);
```

# Open your API

Maybe you want to allow other websites to use your service.

## Allow cross-domain requests

By default, your API is only reachable from a request created from your own domain. If you want to allow people use your API, allow Cross-XHR in your HTTP header:

Access-Control-Allow-Origin: *

You can also allow just a pre-defined list of domains.

Read about [Cross-Origin Resource Sharing](http://hacks.mozilla.org/2009/07/cross-site-xmlhttprequest-with-cors/).

## postMessage

(Thanks to [Daniel Goodwin](http://twitter.com/dsg) for this tip.)

Also, listen to messages sent from [ postMessage](https://developer.mozilla.org/en/DOM/window.postMessage). You could allow people to use your API through postMessage:

```
document.addEventListener("message", function(e){
// retrieve parameters from e.data
var key = e.data.key;
var name = e.data.name;
var dataurl = e.data.dataurl;
// Upload
}
// Once the upload is done, you can send a postMessage to the original window, with URL
```

*That's all. If you have any other tips to share, feel free to drop a comment.*

**Enjoy ;)**

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 40 comments

Mathias BynensJanuary 5th, 2011 at 04:16stefsJanuary 5th, 2011 at 06:01John DrinkwaterJanuary 5th, 2011 at 06:06Bohdan GanickyJanuary 5th, 2011 at 06:23Han Lin YapJanuary 6th, 2011 at 04:13arnoJanuary 5th, 2011 at 06:27JKMJanuary 5th, 2011 at 07:06MikkelJanuary 5th, 2011 at 09:26RichardJanuary 5th, 2011 at 08:52tehkJanuary 5th, 2011 at 08:56thinsoldierJanuary 5th, 2011 at 13:42Jesper KristensenJanuary 5th, 2011 at 09:51Paul IrishJanuary 5th, 2011 at 10:11thinsoldierJanuary 5th, 2011 at 13:40Justin DolskeJanuary 5th, 2011 at 14:45Paul RougetJanuary 6th, 2011 at 03:35AnonymousJanuary 5th, 2011 at 14:50KaiJanuary 5th, 2011 at 15:07Daniel GoodwinJanuary 5th, 2011 at 18:39dimkalinuxJanuary 6th, 2011 at 10:47Johannes FahrenkrugJanuary 6th, 2011 at 11:58Ryan GaspariniJanuary 6th, 2011 at 18:22Brian GrinsteadJanuary 6th, 2011 at 22:11LocJanuary 13th, 2011 at 13:15Stephen FluinJanuary 15th, 2011 at 09:12SimonJanuary 15th, 2011 at 09:41HariFebruary 25th, 2011 at 13:40Paul RougetFebruary 26th, 2011 at 05:29SimonFebruary 26th, 2011 at 01:29SimonMarch 4th, 2011 at 04:59DarylApril 23rd, 2011 at 18:57stefsApril 25th, 2011 at 15:51CobaltBlueDWFebruary 10th, 2012 at 11:43CobaltBlueDWFebruary 11th, 2012 at 19:57Sabith PockerApril 9th, 2012 at 00:05Ashley SheridanOctober 23rd, 2012 at 08:08OSPMarch 7th, 2013 at 05:46mete kavrukApril 5th, 2013 at 13:04Sabith PockerApril 8th, 2013 at 14:13mete kavrukApril 9th, 2013 at 09:34