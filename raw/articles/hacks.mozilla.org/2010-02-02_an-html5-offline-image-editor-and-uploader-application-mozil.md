---
title: an HTML5 offline image editor and uploader application – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2010/02/an-html5-offline-image-editor-and-uploader-application/
author: Paul Rouget
published: '2010-02-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Many web applications use image uploaders: image hosting websites, blog publishing applications, social networks, among many others. Such uploaders have limitations: you can’t upload more than one file at a time and you can’t edit the image before sending it. A plugin is the usual workaround for uploading more than one image, and image modifications are usually done on the server side, which can make the editing process more cumbersome.

Firefox 3.6 offers many [new Open Web features](https://developer.mozilla.org/en/Firefox_3.6_for_developers) to web developers, including even more HTML5 support. This post describes how to create a sophisticated image editor and uploader built using Open Web technologies.

See below for a video of the demo with some background.

## Hosted on hacks, publishes to twitpic

Our web application uploads pictures to twitpic, an image hosting service for Twitter.

Note that code for this application is actually hosted on the [hacks web server](http://hacks.mozilla.org/) but can still upload to Twitpic. Uploading to Twitpic is possible because they opened up their API to [Cross Domain XMLHttpRequests](https://developer.mozilla.org/En/HTTP_Access_Control) for applications like this. (Thank you [twitpic](http://twitpic.com)!).

## Web Features

The [demo](http://demos.hacks.mozilla.org/openweb/imageUploader/) uses the following features from HTML5 included in Firefox 3.6:

[HTML5 Drag and Drop](http://hacks.mozilla.org/2009/12/file-drag-and-drop-in-firefox-3-6/): You can drag and drop items inside of the web page and drag images from your desktop directly into the browser.[HTML5](http://hacks.mozilla.org/2009/06/localstorage/): to store the image data across browser restarts`localStorage`

[HTML5 Application Cache](http://hacks.mozilla.org/2010/01/offline-web-applications/): This allows you to create applications that can be used when the browser isn’t connected to the Internet. It stores the entire app in the browser and also gives you access to online and offline events so you know when you need to re-sync data with a server.[HTML5 Canvas](http://hacks.mozilla.org/2009/06/pushing-pixels-with-canvas/): The HTML5 Canvas element is used through this demo to edit and render images.[Cross-Origin Resource Sharing](http://hacks.mozilla.org/2009/07/cross-site-xmlhttprequest-with-cors/)to host an application at one site and publish data to another.

## What’s in the demo?

See the [live demo](http://demos.hacks.mozilla.org/openweb/imageUploader/) to try the image uploader for yourself. You will need [Firefox 3.6](http://www.firefox.com) and a [twitter](http://twitter.com/) account.

Here’s a full list of the things that this application can do:

- You can drag images from your desktop or the web into the application.
- You can see a preview of each image you want to upload.
- You can drag previews to the trash to delete an image.
- Images are automatically made smaller if they are bigger than 600px wide.
- You can edit any of the images before uploading. This includes being able to rotate, flip, crop or turn an image black and white.
- If you edit an image it’s saved locally so you can still edit when you’re offline. If you close the tab, restart Firefox or your computer they will be there when you load the page again so you can upload when you’re re-connected.
- It will upload several files at once and provide feedback as the upload progresses.
- The HTML5 Offline Application Cache makes the application load very quickly since it’s all stored offline.

## Under the Hood

Let’s quickly go over all of the technology that we’re using in this application.

### Cross-XMLHttpRequest

[Twitpic](http://twitpic.com/) was nice enough to open their API to allow XMLHttpRequests from any other domain. This means that you can now use their API from your own website and offer your own image uploader.

If you’re running a web site with an API you want people to use from other web sites, you can do that with [Cross-site HTTP requests](https://developer.mozilla.org/En/HTTP_Access_Control). In order for you to support it you will need to add an HTTP header to responses from your web server that says which domains you allow. As an example, here’s how twitpic allows access from all domains:

Access-Control-Allow-Origin: *

It’s important to note that opening your API does have security implications so you should be careful to understand those issues before blindly opening an API. For more details, [see MDC documentation on CORS](https://developer.mozilla.org/En/HTTP_access_control).

### Drag and Drop

[Drag and Drop](https://developer.mozilla.org/En/DragDrop/DataTransfer) is a mechanism with two important features:

- Dragging files from your Desktop to your web page.
- Native Drag and Drop inside your web page (not just changing the coordinates of your elements).

The image uploader uses Drag and Drop to allow the user the add files from the Desktop, to remove files (drag them to the trash) and to insert a new image into a current image.

For more on [Drag and Drop](http://hacks.mozilla.org/category/drag-and-drop/), see previous hacks articles, in particular [how to use Drag and Drop in your application](http://hacks.mozilla.org/2009/12/file-drag-and-drop-in-firefox-3-6/).

### Canvas to Edit Images

Once images have been dragged and dropped into the web page, the image uploader lets you edit them before uploading. This is possible because images are actually copied to `canvas`

elements via the [File API](http://hacks.mozilla.org/category/fileapi/).

In this case, the editing process is really basic: rotate, flip, add text, black and white, crop. However, you can imagine offering many other features in your version of the editor (see [Pixastic](http://editor.pixastic.com/) for example, or this inlay feature [here](http://people.mozilla.com/~prouget/demos/fennec/imgManipulation/)).

Using `canvas`

and the [File API](http://hacks.mozilla.org/category/fileapi/) also let you resize the image before sending it. Here, every image is converted to a new image (canvas) that is less than 600px.

### localStorage: Save Local Data

It’s possible to [store local data](http://hacks.mozilla.org/2010/01/offline-web-applications/) persistently in a web page using `localStorage`

, up to 5Mb of data per domain.

In the image uploader, localStorage is used to store images and credentials. Since images are actually `canvas`

, you can store them as data URLs:

```
var url = canvas.getContext("2d").toDataURL("image/png");
localStorage.setItem("image1", url);
```

LocalStorage support means that you can edit an image, close Firefox, switch off your computer, and the edited image will still be there when you restart Firefox.

### Offline

If you add a manifest file listing all remote files needed to display your web application it will work even when you aren’t connected to the Internet. A nice side effect is that it will also make your application load much faster.

Here, the `html`

element refers to a manifest file:

```
```

And the manifest file looks like:

CACHE MANIFEST # v2.4 index.xhtml fonts/MarketingScript.ttf css/desktop.css css/fonts.css css/mobile.css [...]

You can also catch offline and online events to know if the connection status changes.

[For more information see our last article about offline](http://hacks.mozilla.org/2010/01/offline-web-applications/).

## Conclusion

Firefox 3.6 allows millions of people to take advantage of modern standards, including HTML5.

The image uploader described here shows how a web page should really be considered as an application since it interacts with your Desktop and works offline.

Here are a few tips for writing your next application using Open Web technologies:

**Allow Cross-XMLHttpRequest:**

If it makes sense for your service, allow people to access your API from a different domain, you’ll be amazed at the apps people will come up with.

**Allow multiple input:**

Let people Drag files to your application and use `<input type="file" multiple="">`

so they can select several files at once. *In this demo, we use a multiple input which is visible only in the mobile version, but for accessibility consideration, don’t forget to use it to propose an alternative to Drag’n Drop.*

**Use native Drag and Drop:**

Drag and Drop mechanisms are usually simulated (updating coordinates on the mousemove event.) When you can, use the native mechanism.

**Use the File API**

To pre-process a file before even talking to a server.

**Support offline**

Store data and use a manifest to make your application data persistent while offline.

**Use Canvas**

Canvas is the most widely implemented HTML5 element. It works everywhere (even if it has to be [simulated](http://code.google.com/p/explorercanvas/)), use it!

*Think “Client Side”*: HTML5, CSS3 and the new powerful JavaScript engines let you create amazing applications, take advantage of them!

We look forward to seeing the great new applications you’ll come up with using Open Web technologies!

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 44 comments

Paul RougetFebruary 2nd, 2010 at 09:10PaulFebruary 2nd, 2010 at 09:16FritzFebruary 2nd, 2010 at 09:48Francisco CollaoFebruary 2nd, 2010 at 10:39SamFebruary 2nd, 2010 at 10:55sep332February 2nd, 2010 at 10:59thinsoldierFebruary 2nd, 2010 at 12:49bohwazFebruary 2nd, 2010 at 17:30RyanFebruary 2nd, 2010 at 17:52Dwight StegallFebruary 2nd, 2010 at 19:09Jigar shahFebruary 2nd, 2010 at 22:53BWRicFebruary 3rd, 2010 at 03:12GourmetFebruary 3rd, 2010 at 04:33Hasan KöroğluFebruary 4th, 2010 at 01:14Paul RougetFebruary 5th, 2010 at 13:26PauloFebruary 6th, 2010 at 16:40JorgeFebruary 9th, 2010 at 07:39Paul RougetFebruary 13th, 2010 at 05:35kedarFebruary 19th, 2010 at 03:52Paul RougetFebruary 22nd, 2010 at 03:05kedarFebruary 22nd, 2010 at 03:25marvinFebruary 27th, 2010 at 04:59JulienFebruary 25th, 2010 at 11:45AnonbuntuMarch 12th, 2010 at 02:24MatthieuMarch 12th, 2010 at 10:19farquaadApril 26th, 2010 at 05:15Paul RougetApril 26th, 2010 at 05:41Komrade KilljoyJuly 28th, 2010 at 05:43Benjamin LuptonOctober 6th, 2010 at 10:13Paul RougetOctober 7th, 2010 at 05:27Sebastian BeckerFebruary 21st, 2011 at 20:01kishore konjetiMarch 1st, 2011 at 21:54Brandone DonnelsonMarch 26th, 2011 at 11:04tikam chandrakarJune 8th, 2011 at 09:14lingJune 30th, 2012 at 11:47batesAugust 27th, 2012 at 01:39SamOctober 4th, 2012 at 06:45lingOctober 4th, 2012 at 12:16SamOctober 26th, 2012 at 00:01